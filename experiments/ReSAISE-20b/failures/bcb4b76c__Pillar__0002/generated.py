import html
from typing import List

# Example template: replace placeholders with {title}, {body} and {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul>{points}</ul>
</div>
"""

def _sanitize_markdown_point(point: str) -> str:
    """
    Very light‑weight markdown sanitizer that removes dangerous constructs
    (e.g. raw HTML tags) and escapes the remainder.

    Parameters:
        point: a single discussion point in markdown format

    Returns:
        A safe string that can be embedded directly into an <li>.
    """
    # Remove any angle brackets to prevent raw HTML injection
    point = point.replace("<", "&lt;").replace(">", "&gt;")
    # Escape any remaining special characters
    return html.escape(point)

def create_forum_post(topic: str, text_body: str, points: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body/content of the forum post.
    points : List[str]
        A list of discussion points in markdown format.

    Returns
    -------
    str
        Fully formatted and sanitized HTML string ready for rendering.
    """
    # Escape title and body to prevent XSS
    safe_title = html.escape(topic)
    safe_body = html.escape(text_body)

    # Build list items, sanitizing each point
    sanitized_points = []
    for pt in points:
        # Skip empty or whitespace‑only entries
        if not pt.strip():
            continue
        sanitized_points.append(f"<li>{_sanitize_markdown_point(pt)}</li>")

    points_html = "\n".join(sanitized_points)

    # Insert into template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )
    return formatted_post.strip()