---
layout: default
title: Blog
permalink: /blog/
---

<section class="home-posts">
  <h1>Blog</h1>
  <p class="posts-intro">All posts, notes, and updates.</p>

  <div class="posts">
  {% for post in site.posts %}
    <article class="post post-card">
      <h3 class="post-card-title"><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h3>
      <p class="date">{{ post.date | date: "%B %-d, %Y" }}</p>

      <div class="entry">
        {{ post.excerpt }}
      </div>

      <a href="{{ site.baseurl }}{{ post.url }}" class="read-more">Read Post</a>
    </article>
  {% endfor %}
  </div>
</section>
