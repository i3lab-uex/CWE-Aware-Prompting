import html
from typing import List

# Predefined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be replaced
# with the sanitized content.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul>{points}</ul>
</div>
"""

def _escape_and_wrap_list(items: List[str]) -> str:
    """
    Escape each item and wrap it in <li> tags.
    Empty items are skipped to avoid empty list elements.
    """
    escaped_items = []
    for item in items:
        # Skip None or empty strings
        if not item:
            continue
        escaped = html.escape(str(item), quote=True)
        escaped_items.append(f"<li>{escaped}</li>")
    return "\n".join(escaped_items)

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str]
) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user‑provided discussion points or options.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Sanitize title, body, and bullet points
    safe_title = html.escape(str(post_title), quote=True)
    safe_body = html.escape(str(post_body), quote=False)

    # Convert bullet points into a list of <li> elements
    safe_points = _escape_and_wrap_list(bullet_points)

    # Build the final HTML using the predefined template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )