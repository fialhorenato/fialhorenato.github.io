---
title: "Launch a Side Project Online: A Low-Cost Hosting Setup"
tags:
  - Software Development
description: "A historical 2020 guide to launching a side project with a domain, VPS, email, and HTTPS, plus what to check before choosing providers today."
last_modified_at: 2026-11-13
layout: single
---

If you enjoy building with new languages and frameworks, you may have a side project waiting to go live. Time and motivation can get in the way, but cost is another common concern.

This is the low-cost setup I used in 2020 to get a small application online. Provider plans and free tiers change, so treat the prices below as a historical example and check each provider’s current terms before signing up.

## The 2020 setup at a glance

- A `.com` domain (or another domain that fits your project)
- A [DigitalOcean](https://m.do.co/c/a35e5b64be59) VPS running Linux, with the 2020 plan I used offering 1 vCPU, 1 GB of memory, 25 GB SSD, and 1 TB of transfer.
- An email-sending service, which I accessed through this [historical signup link](http://eepurl.com/c3xOub)
- A [domain mailbox](https://www.zoho.com/workplace/pricing.html?src=zmail) (the plan I used then listed 5 GB per user).
- A [service such as Cloudflare](https://www.cloudflare.com/) for DNS, HTTPS, and caching

At the time, the domain’s first-year promotional price was under $1, while credits covered the server temporarily. The recurring server cost still applied after the credit ended.

## How I put the setup together

### 1. Register a domain

In 2020, I searched for introductory .com registration offers and found one advertised for $0.90 for the first year. Promotional prices and renewal rates vary, so compare the full renewal cost before buying:

![Screenshot of a search for discounted domain registration offers](/images/domaincomsearch.png "Historical domain search")

After checkout, I had a .com domain for the promotional price.

**Historical domain price in 2020: $0.90**

### 2. Provision a server

I used a DigitalOcean virtual private server. The article’s linked plan and price reflect the options I saw in 2020; check the provider’s current pricing before choosing a server.

At the time, the plan I used cost $5 per month and included:

- 1 GB memory
- 1 vCPU
- 25 GB SSD storage
- 1 TB transfer

The referral offer linked in the original article provided $100 in promotional credits for two months at the time. Offers change and may not be available to every account or region.

After creating an account, I created a Droplet by choosing a plan, region, and Linux distribution in the control panel.

After creating the Droplet, add the domain to DNS and point its records to the Droplet’s IP address.

If you use the provider's nameservers, copy them from the control panel and set them at your domain registrar. DNS changes can take time to propagate.

Once DNS has propagated, the domain can resolve to the server. The $0.90 figure covered only the domain's first-year promotional price; the server was a recurring charge, temporarily offset by promotional credit.

**Historical server price in 2020: $5/month**

### 3. Configure outbound email

Many applications need to send email, whether for account verification or notifications. In this 2020 setup, I used [Mailchimp](http://eepurl.com/c3xOub). Check the provider’s current plans and sending limits before relying on this option.

At the time, the plan advertised up to 12,000 emails per month and a rate limit of 250 per hour. Those historical limits may no longer apply; confirm current sending quotas and acceptable-use rules with the provider.

At the time, setup involved creating an account and configuring SMTP credentials in the application. Follow the provider’s current setup instructions and protect credentials as secrets.

**Historical plan in 2020: free tier used**

### 4. Set up a domain mailbox

For an inbox on your domain, I used [Zoho Mail](https://www.zoho.com/workplace/pricing.html?src=zmail). Its free plan, storage, and domain limits may have changed; check the current plan details before relying on them.

**Historical plan in 2020: free tier used**

### 5. Configure HTTPS

HTTPS protects traffic between visitors and your site. I used [Cloudflare](https://www.cloudflare.com/) for TLS and caching. Its features and plan limits can change; see the current [product overview](https://www.cloudflare.com/overview/).

After that, I delegated DNS to Cloudflare and configured the required records and TLS settings. Follow the current setup instructions from your registrar and Cloudflare, since dashboard steps and defaults can change.

**Historical plan in 2020: free tier used**

## What this setup cost in practice

This setup involved several separate services. At the time, it provided:

- A .com domain
- A server with 1GB, 1 vCPU and 25GB SSD
- A web application served over HTTPS, with caching configured.
- An outbound email service and a mailbox for the domain.

The domain’s initial promotional price was $0.90, while hosting credit covered the server for a limited period. Recurring costs applied after that. Estimate renewal and ongoing service costs—not just signup prices—before launching.

Before adopting a similar setup today, compare recurring renewal costs, email sending and mailbox limits, backup plans, firewall and access controls, and the operational work of maintaining a VPS. The goal here is to document one historical low-cost path, not to claim that the same providers or prices remain the best option.

If you are launching a side project today, verify prices and plan limits directly with providers before committing.
