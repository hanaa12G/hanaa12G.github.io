---
layout: default
title: Setting up the blog
author: Hana Saitou (hanasou)
status: Incomplete
---


## The reason

  Recently I noticed that Linkedin has blocked my blog page, which I host using   
Cloudflare. Secondly, I'm in need to post my coding stream, but doing so on Linkedin  
will cause trouble: it notifies my connections if that's the post I make after  
a long time. I'm a lowkey person anyway, and there isn't any button that help me  
hide the post for a while.

I asked ChatGPT so show me some step to buy a domain and move my blog there. It  
told me that I need to do these following:
  * Buy a domain.
  * Register domain in DNS.
  * Connect my blog to this domain

## Todos

- [X] Choose domain name
- [ ] ~~Set up Coinbase (for PorkBun payment)~~
- [X] Buy domain
- [X] Setup DNS
- [X] Learn DNS concept
- [X] Add a certificate to my domain
- [X] Jekyll: Make photos visible in final blog post
- [ ] Jekyll: Make photos have reasonable size, or some way to adjust their size
- [ ] Overwrite old github page with this page

## Buying a domain

I read a Reddit thread to find suggestions. Although Cloudflare can be a good
candidate, but I want to try other alternatives, and I see there's a vendor named
Porkbun and it looks promising (also the name is funny).

What should I choose for my domain? I can think of something start with my username:
hanasou. Looks like I have several options, but these 3 looks promising despite 
their price
  * `.dev`: site is related to technology, especially to software developement.
  * `.blog`: site is focused to blogging, used by content creator and influencers
    to share ideas, stories, etc.
  * `.org`: used to present organization, but this is a single person stuff

**I think I can go with `hanasou.dev`**, this blog as far as I can imagine it, maybe
2 months in the future, will only host content for software engineer and programmer
related content.

## Setting up DNS

Looks like Porkbun support DNS setting directly to Cloudflare. I try add a CNAME
to point to my github page like this
  ```text
  CNAME hanasou.dev https://hanaa12g.github.io
  ```

... and it yeild this error
  > Sorry, you can't have a CNAME on the root domain. It violates RFC, will break things, and probably cause your own personal space time to collapse in on itself.
  > You probably want to use an ALIAS record instead.

A quick search show that hanasou.dev is a root domain, so we should make it a A
record instead, it makes sense to me root domain should link to some exact IP address.

Let me follow the error suggestion. Adding a ALIAS record like this:
  ```text
  ALIAS hanasou.dev hanaa12.github.io
  ```
... and it yield this error:

  > ERROR: Could not add DNS record: An A, AAAA, ALIAS, or CNAME record with that host already exists. 

Ah, I see, at the bottom of the page there're 4 records already: 2 created by default
from Porkbun, 2 were created by me when I tested them out. I removed all the records
and add these 2 following lines

  ```text
  CNAME www.hanasou.dev hanaa12g.github.io
  ALIAS hanasou.dev hanaa12g.github.io
  ```

... and there isn't any error show this time.

Tested this out and this is what I get ![screenshot](/assets/images/screenshots/invalid_certificate_domain.png)

## Add a certificate to `hanasou.dev`

Looks like they handle this for me, great! Let's wait for a few day

![image](/assets/images/screenshots/porkbun_ssl_certificate_notice.png)

## But I want to visit the page, is there a way to access?

Nevermind, just after a few minutes it actually enable https for my page

## Jekyll

Let store screenshot for this blog somewhere. Jekyll documentation page says that
we can store in `assets` directory and the files will be automatically copied when
we deploy. That's good. Then I use the syntax `![imgaee](url)` to actuall display
the image. But man it's very large.
