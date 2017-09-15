---
layout:     post
title:      How to put your sideproject online with less than $6
description: How to kick your sideproject with only $6
lang: en-US
author: "Renato Fialho"
---

If you are an enthusiast of development, new languages or new frameworks, there's a 99% chance that you have a Side-Project waiting to be kicked off, and probably for laziness, lack of time or lack of money, you don't want to put it in production.

But don't worry, that happens very often.

On this post, i will talk about the reason which is probably the biggest reason why developers are resistant to put those projects in production : Money.

Well, that's our setup:

- A [.com](https://www.google.com/search?q=.com+domains+sale&oq=.com+domains+sale&gs_l=psy-ab.3..0i22i30k1l4.933.1276.0.1422.5.4.0.0.0.0.229.229.2-1.1.0....0...1.1.64.psy-ab..4.1.227.L1LdrHkPymY){:target="_blank"} domain of your choice
- A [DigitalOcean](https://www.digitalocean.com/){:target="_blank"} VPS using Linux (Distro of your choice) with 1 vCPU, 512MB of memory, 20GB SSD and 1TB of transfer.
- A SaaS who helps you send your e-mails (12k/mo or 250/hour)
- A mailserver with 5GB of space per user, 10 users max.
- A SSL solution (https certificate)

Wait? What? For $6?

## Show me that magic!

### First step: Domain Purchase

Do you usually click on Adwords ads on google searches? Me neither. 

But on this case, the main goal is to [look at those ads](https://www.google.com/search?q=.com+domains+sale&oq=.com+domains+sale&gs_l=psy-ab.3..0i22i30k1l4.933.1276.0.1422.5.4.0.0.0.0.229.229.2-1.1.0....0...1.1.64.psy-ab..4.1.227.L1LdrHkPymY){:target="_blank"} and find our gold pot.

Go to google and type "domain .com sale" and look at the ads:

{: .center}
![alt text center](/images/domaincomsearch.png "Search for cheap domains on google")

Domains for $0.90/yr? Deal!

After the checkout steps and process, *voala*, you have your new .com domaing for $.90 cents!

### Second step: The Server

Have you ever heard about DigitalOcean? In my opinion, they give you the cheapest and with the best benefits server that you can have. For small or large applications.

{: .center}
![alt text center](/images/digitalocean.png "Digital Ocean Pricing")

That means, with $5 per month you can have a server with:

- 512MB Memory
- 1 vCPU
- 20GB SSD Disk
- 1TB Transfer

But, as i want you to suceed, there's a [**DISCOUNT COUPON**](https://m.do.co/c/a35e5b64be59){:target="_blank"} that gives you $10, or 2 months **FOR FREE!**

After creating an account from the link, you can create an account and from your control panel, you can creat a droplet choosing your plan, region and distro.

*PS: There's a lot of "1 click apps" that DigitalOcean provides as WordPress, Rails and many others. Before choosing your distro, go to that area to see if they already have what you need*

After creating your droplet, go to the DNS menu and add your domain, putting your droplet's IP. Copy the 3 nameservers (NS1.digitalocean.com ...) and change on your domain control panel.

Wait a little for the DNS to reflect the changes and Done! You have a domain and a server to run your application! And we spent only $5.90!


### Third step: Hiring e-mail servers

Pretty much all application need to send e-mails, right? It can be a sign up e-mail or only notifications. So for that we chose [MailChimp](http://eepurl.com/c3xOub){:target="_blank"}.

Using the service, you can send 12k e-mails trough SMTP per month, or 250 per hour! **FOR FREE!**

{: .center}
![alt text center](/images/mailchimp.png "MailChimp Pricing")

MailChimp is very simple, you create an account and it's almost ready.

On this step, we gonna hire an e-mail server too, so we can have a nice me@mydomain.com.

And for that, we gonna use [ZohoMail](https://www.zoho.com/workplace/pricing.html?src=zmail){:target="_blank"}, which offers us 5GB space per account, limited to 25 accounts and 1 domain **FOR FREE**

{: .center}
![alt text center](/images/zohomail.png "Zoho Mail Pricing")

Go ahead and create your account, but we have another step before finishing.

### Fourth step: Getting SSL (https://...)

Is very important to keep your information safe, and having a SSL setted up in our application will help a lot!

We gonna use [CloudFlare](https://www.cloudflare.com/){:target="_blank"}. It gives us SSL **FOR FREE** ! (It takes around 48 hours to be activated).

Cloudflare offers us another functions too, as assets cache, optimization, DDoS prevention, you can check everything [here](https://www.cloudflare.com/overview){:target="_blank"}

Vamos utilizar a CloudFlare . Ela nos oferece SSL de graça ! ( Demora em torno de 48h para ser ativado) e inúmeras outras funcionalidades como cache de assets, optimização, prevenção contra DDOS. Veja todas as vantagens aqui: https://www.cloudflare.com/overview

After that you need to change your NS servers to cloudflare and some further settings, but everything is explained on each service website.

### Conclusion

Well, it took some time, but after everything you have:

- A .com domain
- A server with 512Mb, 1 vCPU and 20GB SSD
- SSL ready
- 2 e-mail servers, 1 for SMTP and other for your inbox

And for how much? $.90 cents for right now and you gonna start spending money in only 2 months, because you have the $10 coupon that i gave to you!

Have fun!