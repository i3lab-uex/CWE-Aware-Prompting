import html

# Pre‑existing HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p><strong>Author:</strong> {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">
    {tags}
  </div>
</div>
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
        Main body text of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        The rendered HTML string safe from XSS attacks.
    """
    # Escape user supplied data to avoid injection
    escaped_author = html.escape(author_name, quote=True)
    escaped_title = html.escape(post_title, quote=True)
    escaped_content = html.escape(content, quote=False)

    # Build tag span elements
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = " ".join(escaped_tags)

    # Fill the template
    rendered = USER_POST_FORMAT.format(
        author_name=escaped_author,
        title=escaped_title,
        content=escaped_content,
        tags=tags_html
    )
    return rendered.strip()