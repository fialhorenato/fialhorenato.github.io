# Foldspace — Protein Structure Explorer

Foldspace is a small, static web app for exploring protein structures from the
[RCSB Protein Data Bank](https://www.rcsb.org/). Enter a four-character PDB ID
to load its coordinates, inspect the structure in 3D, and see a compact summary
of chains, residues, atoms, and non-water ligand groups.

## Run locally

Open `index.html` directly or serve this directory locally. The interaction
map data is bundled in `interaction-data.js`, so it also works when opened from
a `file://` URL. Loading PDB coordinates requires an internet connection; the
page retrieves them from RCSB and loads 3Dmol.js from its official host. No
build step or package manager is needed.

You can share a direct link to a structure with `?pdb=1BGA` appended to the
page URL.

## Live residue contact map

When you load a PDB ID, the browser uses the same coordinate file it downloads
from RCSB to calculate a residue contact network in memory. It considers
standard protein atoms, excludes contacts between residues within two sequence
positions on the same chain, and groups atom pairs at or below 5 Å into residue
pairs. Pairs with atom distances at or below 3.5 Å are labeled “Close contact”;
the remainder are “Proximity”. These are geometric distance classes, not
chemically assigned hydrogen bonds or other interaction types. A spatial grid
keeps the calculation practical for larger structures. The project’s original
precomputed 1BGA analysis remains available when the page is opened without a
PDB ID or if no live structure is loaded.

```sh
Open index.html?pdb=1BGA
```

## Optional offline data generation

`generator.py` can still convert existing contact CSV data into a bundled
`interaction-data.js` dataset for offline viewing. The live map does not need
Python or a COCaDA request.

The page also keeps the original project idea: a filterable residue interaction
network, with search, interaction-type filters, and Cinema, Clustal, and Lesk
color schemes. When a PDB ID is entered, the network is derived from that
entry’s coordinates; the bundled original 1BGA map remains as the offline
default.

## Sources and dependencies

- Molecular rendering: [3Dmol.js](https://3dmol.org/), loaded from the official
  hosted build.
- Structure coordinates and live contact-map input: [RCSB PDB](https://www.rcsb.org/).
- Mounted interaction graph: `interaction-data.js` (a JavaScript object so
  browsers can load it from `file://`).

This project no longer needs the old D3, jQuery, Bootstrap, or color-picker
libraries. The bundled map starts with the original 1BGA contacts and can be
replaced with a generated PDB map. Its data is stored at residue level instead
of the old atom-level graph. Counts in the structure summary are calculated
from the PDB coordinate records shown in the viewer;
they are intended as a quick overview, not a substitute for the entry's curated
metadata.
