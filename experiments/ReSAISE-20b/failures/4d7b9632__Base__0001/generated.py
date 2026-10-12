import html

# Predefined template with placeholders for the post components.
USER_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h2>{title}</h2>
    <p class="author">Posted by {author_name}</p>
  </header>
  <section class="content">
    {body}
  </section>
  <footer class="tags">
    {tags}
  </footer>
</article>
"""

def render_forum_post(author_name: str,
                      title: str,
                      body_content: str,
                      tag_list: list[str]) -> str:
    """
    Generate a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        A string containing the sanitized HTML of the forum post.
    """
    # Escape user‑supplied data to prevent XSS attacks
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)

    # Wrap each tag in a <span> element and escape the tag text
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    ]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )