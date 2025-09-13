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
<details>
<summary>Click to expand</summary>

{% capture md %}
- [X] Choose domain name
- [ ] ~~Set up Coinbase (for PorkBun payment)~~
- [X] Buy domain
- [X] Setup DNS
- [X] Learn DNS concept
- [X] Add a certificate to my domain
- [X] Jekyll: Make photos visible in final blog post
- [ ] Jekyll: Make photos have reasonable size, or some way to adjust their size
- [X] Overwrite old github page with this page
- [O] Jekyll: Draft for a style
    - [X] Collect some ideas
    - [ ] ~~Jekyll: Design a landing page~~
    - [X] Choose a font
    - [X] Define theme with basic color scheme
    - [X] Code highlighter
    - [ ] ~~Update navigation bar~~
    - [X] Tags page
    - [X] Last updated
    - [X] Store image in cloud
- [.] Jekyll: Created pin post/sections for streaming/notification
    - [X] Jekyll: Find out how to separate pin post
    - [ ] Jekyll: Design root page
{% endcapture %}
{{ md | markdownify }}

</details>

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
  >
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

Tested this out and this is what I get ![screenshot](https://drive.google.com/thumbnail?id=1KR9q-Ohodtan8YS4CO8XONYHhdj5Bxg7&sz=w1920-h1080)

## Add a certificate to `hanasou.dev`

Looks like they handle this for me. After like 10 minutes I the previous error was
gone
![image](https://drive.google.com/thumbnail?id=1COUYQe1gh4R-RNaYWk3mDIgY8WC4ZwrE&sz=w1920-h1080)

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

1. [kube.io](https://kube.io/blog/liquid-glass-css-svg)
2. [dbos.dev](https://www.dbos.dev/blog/durable-queues)
3. [glfmm.io](https://glfmn.io/posts/zig-error-patterns/)
4. [ciesie.com](https://ciesie.com/post/tagged_unions/)
5. [stopa.io](https://stopa.io/post/297)
6. [xeiaso.net](https://xeiaso.net/)
7. [maurycyz.com](https://maurycyz.com/misc/ads/)

### Jekyll: Code highlighter

Markdown code and code block is rendered into HTML `<code>` element, with one difference:
code block has nested inside a `<div><pre>` tree.

To select 2 types of code, I use this selector:
```css
/* Select code block */
div:has(> pre > code) {}
/* Select inline code */
:not(pre) > code  {}
```

We only have language information when we're using code block, with inline code
the language is unknown. We can have different highlighting style for each language.
But Jekyll, which uses Kramdown, which then use Rouge syntax highlighter to highlight
the text. HTML element within code block has several classes:
    * `.c` for comment ??
    * `k` for keyword
    * `nf` for function
    * .etc
Which I can not find an obvious documentation for it, they way many tutorials
point me to use is to generate a pre-defined using Rouge as well. So I generated
Monokai syntax highlighter and put into output html. 
```bash
rougify style monokai > assets/css/code_highlight.css
```
And it just works, if you read this block later and the style is not monokai, either
I use different style or I overwritten some color in that file.


### Jekyll: Tags page

Jekyll supports tags under `page.tags`, and they only for display. I want it to
to have a little more feature: Filtering post by tags, when user clicks on a tag
it will send us to a page that show all the posts having this tag. From my research,
Jekyll doesn't support this automatically, as Jekyl only serve pages statically, and
adding a new tag won't rerender the page. We either rely on javascript to filter
posts, but I don't want to mess with javascript at the moment because it hook me
up on doing some page animation!

I come up with a solution: Render each filter page by script. I wrote a python
script that I will run periodically, this script will scan all the tags and render
a file under `tag/<tag_name>html`. Content of all page are almost the same, they
only differ a single Front Matter property named `tag`. Each page will include a
template I prepared beforehand, passing the tag. The template will then filter to
only render matched post from every post of the site.

### Jekyll: Store image

I use Google Drive to store my image, but there's a catch, Google does not allow
us to embed direct link to image url. We can only use an `<iframe>` on our site to
display it. This may goes againts my normal way of rendering image by `<img>`. Haven't
try using `<iframe>` yet but I work around it from this [stack overflow question](https://stackoverflow.com/questions/15557392/how-do-i-display-images-from-google-drive-on-a-website).

The output images are not in high quality but they're enough for casual views. If
I ever want to share a HD image I will put the link under the image itself.
