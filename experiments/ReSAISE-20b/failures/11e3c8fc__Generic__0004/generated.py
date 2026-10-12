import html

# Predefined HTML template with placeholders for the post components.
USER_POST_FORMAT = """
<article class="blog-post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <footer class="tags">
    {labels}
  </footer>
</article>
"""

def render_blog_post(author_id: str, post_heading: str, content: str, labels: list[str]) -> str:
    """
    Generate a secure HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        The heading/title of the post.
    content : str
        Main body text of the post.
    labels : list[str]
        Tags/labels associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for the post.
    """
    # Escape all user supplied data to prevent XSS attacks.
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Render each label inside a <span> and escape its content.
    safe_labels = []
    for lbl in labels:
        escaped_lbl = html.escape(lbl)
        safe_labels.append(f'<span class="tag">{escaped_lbl}</span>')

    labels_html = " ".join(safe_labels)

    # Fill the template with sanitized values.
    return USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=labels_html
    )