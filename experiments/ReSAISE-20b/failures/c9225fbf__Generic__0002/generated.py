import html

# A simple template that the user can modify.  It must contain the four placeholders:
#   {author_name}, {post_title}, {content}, and {tags_html}
USER_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h1>{post_title}</h1>
    <p class="author">Posted by: {author_name}</p>
  </header>
  <section class="content">
    {content}
  </section>
  <footer class="tags">
    {tags_html}
  </footer>
</article>
"""

def create_post_html(author_name: str,
                     post_title: str,
                     content: str,
                     post_tags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the user who created the post.
    post_title : str
        Title/headline of the post.
    content : str
        Main body text of the post.  It may contain user‑supplied HTML that must be escaped.
    post_tags : list[str]
        List of tags associated with the post.  Each tag will be wrapped in a <span>.

    Returns
    -------
    str
        A string containing the escaped and formatted HTML for the post.

    Notes
    -----
    * All user supplied strings are escaped using `html.escape` to prevent XSS.
    * The function does not perform any further validation on the tag names; it simply
      escapes them and places each inside a <span> element.
    """
    # Escape user input to avoid injection
    safe_author = html.escape(author_name, quote=True)
    safe_title  = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the tags section
    escaped_tags = [f'<span class="tag">{html.escape(tag, quote=True)}</span>'
                    for tag in post_tags]
    tags_html = ' '.join(escaped_tags)

    # Fill the template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        post_title=safe_title,
        content=safe_content,
        tags_html=tags_html
    )