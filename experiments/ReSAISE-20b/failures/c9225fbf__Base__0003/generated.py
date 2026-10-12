import html

# Example template; adjust placeholders as needed.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">{tags}</div>
</div>
"""

def create_post_html(author_name: str, post_title: str,
                     content: str, post_tags: list[str]) -> str:
    """
    Build an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the post's author.
    post_title : str
        Title of the forum post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering.
    """
    # Escape all user‑supplied content
    safe_author = html.escape(author_name, quote=True)
    safe_title  = html.escape(post_title,  quote=True)
    safe_content= html.escape(content,   quote=False)  # Preserve line breaks

    # Build tag string; each tag is wrapped in a <span>
    safe_tags = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Format the final HTML
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )