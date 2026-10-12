import html

# Example template – in real use this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p><strong>Author:</strong> {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">{tags}</div>
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
        The name of the post's author.
    post_title : str
        The headline of the user's post.
    content : str
        The primary text content of the user's post.
    post_tags : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        The HTML string for the post, with all user supplied data escaped.

    Raises
    ------
    ValueError
        If any of the required arguments are None.
    """
    # Basic sanity checks
    if author_name is None or post_title is None or content is None or post_tags is None:
        raise ValueError("All arguments must be provided and non‑None")

    # Escape all user supplied strings to avoid injection (CWE‑74)
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build tag list – each tag is escaped and wrapped in a <span>
    safe_tags = ""
    for tag in post_tags:
        if tag is None:
            continue
        escaped_tag = html.escape(str(tag), quote=True)
        safe_tags += f'<span class="tag">{escaped_tag}</span> '

    # Strip trailing space
    safe_tags = safe_tags.strip()

    # Format the final HTML using the template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )