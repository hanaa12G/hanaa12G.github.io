---
layout: blog
title: Setting up the blog (New)
author: Hana Saitou (hanasou)
status: Incomplete
---


## The reason {#my_class}

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
- [X] Overwrite old github page with this page
- [ ] Jekyll: Draft for a style
    - [ ] Collect some ideas
    - [ ] Jekyll: Design a landing page
    - [ ] Choose a font
    - [ ] Define theme with basic color scheme
- [.] Jekyll: Created pin post/sections for streaming/notification
    - [X] Jekyll: Find out how to separate pin post
    - [ ] Jekyll: Design root page

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

### Store screenshot

Let store screenshot for this blog somewhere. Jekyll documentation page says that
we can store in `assets` directory and the files will be automatically copied when
we deploy. That's good. Then I use the syntax `![imgaee](url)` to actuall display
the image. But man it's very large.

### Pin post

Document doesn't mention how to customize the post, but I see something interesting
within the code example.
{% raw %}
```html
<h1>My blog posts</h1>
<ul>
  {% for post in site.posts %}
  <li>
    <h2><a href="{{ post.url }}"> {{ post.title }}</a></h2>
    {{ post.excerp }}
  </li>
  {% endfor %}
</ul>
```
{% endraw %}



`site.posts` are mentioned in documentation, and each `post` should be a Post object.
Then in the loop it access `post.url`, `post.title`, and `post.excerp`. When I open
each post page, it use *front matter* to define some meta data for a page, including
`title`. So I immediately thought that: what if I add a `pin: True` in that section
and access it in the index page. Like this
{% raw %}
```html
<!-- same as before -->
  <li>
    <h2><a href="{{ post.url }}"> {{ post.title }}</a></h2>
    {{ post.pin }}
  </li>
<!-- same as before -->
```
{% endraw %}

It works as I expect, now I can modify each page and mark them pinned. And in `post.html`
I need to separate them into 2 different list. First list containing pinned post
should be display first and stay in top (sidebar)

{% raw %}

```c++
int main(int argc, char** argv) {
    return 0;
}
```

{% endraw %}

### Code block is replaced by Jekyll

The example above was not able to display correctly if I don't add raw/endraw tags
because by default Jekyll will process Liquid everywhere. 


### Collecting some ideas for my site

This section also keeps the link to some amazing blog I came across today, I haven't
had time to read each acticle entirely but will come back once my task is done.

#### [kube.io](https://kube.io/blog/liquid-glass-css-svg)

This site has simple and straight landing page. Landing page is contained within
a single page, so we don't need scrolling. The "Hero Section" is just a heading
element that says "Hello. I build software & design". Below "Hero Section" is the
list of most recent posts and then the contact information. This entire landing
page is fit inside the content area and does not span the window's width.

![Landing page](/assets/images/screenshots/kube_io_landing_page.png)


Rating the color, This site choose a simple combination of colors: dark background,
white-ish for foreground and a blue-purple color for links, highlighted, keywords,
and code section.

The animation is a nice when I hover on the logo, it spins when I click. The logo
is a cube which I think I've seen this kind of design somewhere.

The font name is: Inter, InterVariable


#### [dbos.dev](https://www.dbos.dev/blog/durable-queues)

I can see this site's purpose is to go commercially when jumped into the landing
page. It has full bleed design. And it got many following sections after the hero:
features, testimonial, footer, etc. But scrolling down I can see this is just an
attempt, and following sections are weird organized and I feel these are just template
they put on to fill in the space. But following the links, it makes me think this
is legit again, a little confusing.

I feel the page has a boxy design, which use a lot of highlighted border. I don't 
recorgnize the color scheme from this site.

Font family: Ibmplexsans, Arial, sans-serif
Landing page:

My rating: 3/5 (Normal)

![landing page](/assets/images/screenshots/dbos-landing.png)

Blog page:

![blog](/assets/images/screenshots/dbos-blog.png)

My rating: 2/5 (Not very bad)


#### [glfmm.io](https://glfmn.io/posts/zig-error-patterns/)


#### [ciesie.com](https://ciesie.com/post/tagged_unions/)



#### [stopa.io](https://stopa.io/post/297)

#### [xeiaso.net](https://xeiaso.net/)


#### [maurycyz.com](https://maurycyz.com/misc/ads/)
