import html

# Pre‑defined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-content">{content}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def build_forum_post(headline: str, content: str, items: list[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post.
    items : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post string.
    """
    # Escape all user‑supplied data to prevent HTML injection (CWE‑74).
    safe_title = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the unordered list safely.
    point_items = []
    for item in items:
        escaped_item = html.escape(item, quote=True)
        point_items.append(f"<li>{escaped_item}</li>")
    safe_points = "\n".join(point_items)

    # Format the final post.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        content=safe_content,
        points=safe_points
    )