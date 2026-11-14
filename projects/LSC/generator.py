#!/usr/bin/env python3
"""Build Foldspace's residue interaction map from an interaction CSV.

The generator can fetch precomputed COCaDA-web contacts by PDB ID or read a
downloaded CSV. It aggregates records by residue pair and interaction type,
then writes a JavaScript data file that index.html can load directly from
file://.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from collections import Counter
from pathlib import Path
from typing import Any


INTERACTION_COLORS = {
    "Aromatic stacking": "#E36262",
    "Hydrogen bond": "#02B7DB",
    "Hydrophobic": "#F0ED67",
    "Repulsive": "#512B8B",
    "Salt bridge": "#519136",
    "Attractive": "#57A9C8",
    "Disulfide bond": "#A8B3BC",
    "Uncertain attractive": "#8AA9B8",
    "Uncertain repulsive": "#9683B5",
    "Uncertain salt bridge": "#79A26F",
}
FALLBACK_INTERACTION_COLOR = "#91A4B4"
COCADA_TYPES = {
    "HB": "Hydrogen bond", "HY": "Hydrophobic", "AT": "Attractive",
    "RE": "Repulsive", "SB": "Salt bridge", "DS": "Disulfide bond",
    "AS": "Aromatic stacking", "UAT": "Uncertain attractive",
    "URE": "Uncertain repulsive", "USB": "Uncertain salt bridge",
}

# Preserve the project's familiar Cinema, Clustal, and Lesk residue palettes.
AMINO_ACID = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}
CINEMA = {
    **dict.fromkeys("HKR", "#1240AB"), **dict.fromkeys("DE", "#BF3030"),
    **dict.fromkeys("NQST", "#9F3ED5"), **dict.fromkeys("AGILMV", "#4EA429"),
    **dict.fromkeys("FPWY", "#009999"), "C": "#FFAA00",
}
CLUSTAL = {
    **dict.fromkeys("GPST", "#FF9640"), **dict.fromkeys("HKR", "#BF3030"),
    **dict.fromkeys("FWY", "#1240AB"), **dict.fromkeys("ILMV", "#008500"),
    **dict.fromkeys("DE", "#BF3030"), **dict.fromkeys("NQ", "#9F3ED5"),
    "C": "#FFAA00", "A": "#9E9E9E",
}
LESK = {
    **dict.fromkeys("AGST", "#FF9640"), **dict.fromkeys("CFILMPVWY", "#269926"),
    **dict.fromkeys("HNQ", "#CD0077"), **dict.fromkeys("DE", "#BF3030"),
    **dict.fromkeys("KR", "#1240AB"), "A": "#FF9640",
}
RESIDUE_COLORS = {"cinema_color": CINEMA, "clustal_color": CLUSTAL, "lesk_color": LESK}

ATOM_PATTERN = re.compile(
    r"^(?:ATOM|HETATM)_\d+_[^_]+_(?P<resname>[A-Za-z0-9]{3})_"
    r"(?P<resid>-?\d+[A-Za-z]?)_(?P<chain>[^_]*)$"
)


def parse_atom_residue(value: str) -> dict[str, str] | None:
    """Extract residue identity from atom names like ATOM_12_CA_GLY_4_A."""
    match = ATOM_PATTERN.fullmatch(value.strip())
    if not match:
        return None
    resname = match.group("resname").upper()
    chain = match.group("chain").strip() or "∅"
    resid = match.group("resid").upper()
    return {
        "resname": resname,
        "resid": resid,
        "chain": chain,
        "key": f"{chain}:{resid}:{resname}",
        "base_name": f"{resname}{resid}",
    }


def make_residue(resname: str, resid: str, chain: str) -> dict[str, str] | None:
    resname = resname.strip().upper()
    resid = resid.strip().upper()
    chain = chain.strip() or "∅"
    if not resname or not resid:
        return None
    return {
        "resname": resname,
        "resid": resid,
        "chain": chain,
        "key": f"{chain}:{resid}:{resname}",
        "base_name": f"{resname}{resid}",
    }


def normalize_interaction(value: str) -> str:
    clean = value.strip()
    return COCADA_TYPES.get(clean.upper(), clean)


def fetch_cocada_csv(pdb_id: str) -> tuple[str, str]:
    """Fetch the public precomputed contact CSV published by COCaDA-web."""
    code = pdb_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{4}", code):
        raise ValueError("PDB ID must contain exactly four letters or digits.")
    url = f"https://bioinfo.dcc.ufmg.br/cocada-web/data/pdb/{code[0]}/{code}/{code}_contacts.csv"
    request = Request(url, headers={"User-Agent": "Foldspace protein explorer/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8-sig")
    except HTTPError as exc:
        if exc.code == 404:
            raise ValueError(
                f"COCaDA-web has no precomputed contact CSV for {code}. "
                "Use a downloaded CSV or run COCaDA locally for this structure."
            ) from exc
        raise ValueError(f"COCaDA-web returned HTTP {exc.code} for {code}.") from exc
    except URLError as exc:
        raise ValueError(f"Could not reach COCaDA-web: {exc.reason}") from exc
    if not text.strip() or text.lstrip().startswith("<"):
        raise ValueError(f"COCaDA-web returned no contact CSV for {code}.")
    return text, f"{code}_contacts.csv"


def build_graph(csv_path: Path | None, pdb_id: str | None, csv_text: str | None = None, source_name: str | None = None) -> dict[str, Any]:
    nodes_by_key: dict[str, dict[str, Any]] = {}
    edge_counts: Counter[tuple[str, str, str]] = Counter()
    edge_distances: dict[tuple[str, str, str], list[float]] = {}
    type_totals: Counter[str] = Counter()
    invalid_rows = 0
    accepted_rows = 0

    if csv_text is not None:
        source = io.StringIO(csv_text, newline="")
    elif csv_path is not None:
        try:
            source = csv_path.open("r", encoding="utf-8-sig", newline="")
        except OSError as exc:
            raise ValueError(f"Cannot open CSV file {csv_path}: {exc}") from exc
    else:
        raise ValueError("Provide a CSV file or a PDB ID to fetch from COCaDA-web.")

    with source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("The CSV is empty or has no header row.")
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
        interaction_column = "interaction" if "interaction" in reader.fieldnames else "type"
        residue_columns = {"chain1", "res1", "resname1", "chain2", "res2", "resname2"}
        cocada_format = residue_columns.issubset(reader.fieldnames)
        if not cocada_format and not {"atom1", "atom2"}.issubset(reader.fieldnames):
            raise ValueError(
                "CSV needs atom1/atom2 columns, or COCaDA columns "
                "Chain1, Res1, ResName1, Chain2, Res2, ResName2."
            )
        if interaction_column not in reader.fieldnames:
            raise ValueError("CSV is missing the interaction or Type column.")

        for row_number, row in enumerate(reader, start=2):
            interaction = normalize_interaction(row.get(interaction_column) or "")
            if not interaction:
                continue

            if cocada_format:
                atom1 = make_residue(row.get("resname1") or "", row.get("res1") or "", row.get("chain1") or "")
                atom2 = make_residue(row.get("resname2") or "", row.get("res2") or "", row.get("chain2") or "")
            else:
                atom1 = parse_atom_residue(row.get("atom1") or "")
                atom2 = parse_atom_residue(row.get("atom2") or "")
            if not atom1 or not atom2:
                invalid_rows += 1
                if invalid_rows <= 5:
                    print(f"Warning: skipping row {row_number}: could not parse residue IDs", file=sys.stderr)
                continue
            if atom1["key"] == atom2["key"]:
                continue

            for residue in (atom1, atom2):
                key = residue["key"]
                if key not in nodes_by_key:
                    one_letter = AMINO_ACID.get(residue["resname"], "X")
                    node: dict[str, Any] = {
                        "name": residue["base_name"],
                        "resname": residue["resname"],
                        "resid": residue["resid"],
                        "chain": residue["chain"],
                        "key": key,
                        "value": 0,
                    }
                    for field, palette in RESIDUE_COLORS.items():
                        node[field] = palette.get(one_letter, "#A8B3BC")
                    nodes_by_key[key] = node
                nodes_by_key[key]["value"] += 1

            keys = sorted((atom1["key"], atom2["key"]))
            edge_key = (keys[0], keys[1], interaction)
            edge_counts[edge_key] += 1
            type_totals[interaction] += 1
            distance_text = (row.get("distance") or row.get("distance_a") or "").strip()
            if distance_text:
                try:
                    distance = float(distance_text)
                    if math.isfinite(distance):
                        edge_distances.setdefault(edge_key, []).append(distance)
                except ValueError:
                    pass
            accepted_rows += 1

    if accepted_rows == 0:
        raise ValueError("No valid residue interactions were found in the CSV.")

    nodes = list(nodes_by_key.values())
    base_name_counts = Counter(node["name"] for node in nodes)
    for node in nodes:
        if base_name_counts[node["name"]] > 1:
            node["name"] = f"{node['name']} · {node['chain']}"
    index_by_key = {node["key"]: index for index, node in enumerate(nodes)}

    links = []
    for (source_key, target_key, interaction), count in edge_counts.items():
        distances = edge_distances.get((source_key, target_key, interaction), [])
        link: dict[str, Any] = {
            "source": index_by_key[source_key],
            "target": index_by_key[target_key],
            "type": interaction,
            "color": INTERACTION_COLORS.get(interaction, FALLBACK_INTERACTION_COLOR),
            "count": count,
        }
        if distances:
            link["distance"] = round(sum(distances) / len(distances), 3)
        links.append(link)

    return {
        "metadata": {
            "pdb_id": pdb_id.upper() if pdb_id else None,
            "source_csv": source_name or (csv_path.name if csv_path else f"{pdb_id.upper()}_contacts.csv"),
            "interaction_records": accepted_rows,
            "skipped_rows": invalid_rows,
            "interaction_types": dict(type_totals),
        },
        "nodes": nodes,
        "links": links,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a PDB-derived residue interaction CSV into a Foldspace map."
    )
    parser.add_argument("csv_file", type=Path, nargs="?", help="Optional downloaded CSV; otherwise fetch by PDB ID")
    parser.add_argument("--pdb-id", help="PDB ID to fetch from COCaDA-web and show on the map")
    parser.add_argument(
        "--output", "-o", type=Path,
        help="JavaScript data bundle path (default: interaction-data.js beside this script)",
    )
    args = parser.parse_args()
    output_path = args.output or Path(__file__).resolve().with_name("interaction-data.js")

    try:
        csv_text = source_name = None
        if args.csv_file is None:
            if not args.pdb_id:
                parser.error("Provide a CSV file or use --pdb-id to fetch contacts from COCaDA-web.")
            csv_text, source_name = fetch_cocada_csv(args.pdb_id)
        graph = build_graph(args.csv_file, args.pdb_id, csv_text, source_name)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
        output_path.write_text(f"window.FOLDSPACE_INTERACTION_DATA = {payload};\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    metadata = graph["metadata"]
    print(
        f"Wrote {len(graph['nodes']):,} residues and {len(graph['links']):,} "
        f"residue-pair links ({metadata['interaction_records']:,} CSV interaction records) "
        f"to {output_path}"
    )
    if metadata["skipped_rows"]:
        print(f"Skipped {metadata['skipped_rows']:,} malformed row(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
