import html
from typing import List

# A simple pre‑defined template for a forum post.
FORUM_POST_FORMAT = """
<h2>{title}</h2>
<div class="forum-body">{body}</div>
<ul class="forum-points">
{points}
</ul>
"""

def _escape_and_trim(text: str) -> str:
    """
    Escape HTML special characters and trim whitespace.
    """
    return html.escape(text.strip())

def _render_points(points: List[str]) -> str:
    """
    Convert a list of markdown‑style points into safe HTML <li> elements.
    Each point is expected to start with a dash or bullet. The function
    removes the leading marker and escapes the remaining text.
    """
    if not points:
        return ""
    rendered = []
    for p in points:
        # Remove common markdown list markers: '-', '*', '+'
        trimmed = p.lstrip(" -*+").strip()
        escaped = _escape_and_trim(trimmed)
        rendered.append(f"  <li>{escaped}</li>")
    return "\n".join(rendered)

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a forum post from the given title, body and discussion points.

    Parameters
    ----------
    title : str
        The forum post's title.
    body : str
        Main content of the post.
    points : list[str]
        Markdown‑style discussion points.

    Returns
    -------
    str
        A fully formatted, sanitized HTML forum post.
    """
    if not isinstance(title, str) or not isinstance(body, str):
        raise TypeError("Title and body must be strings.")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise TypeError("Points must be a list of strings.")

    safe_title = _escape_and_trim(title)
    safe_body = _escape_and_trim(body)
    rendered_points = _render_points(points)

    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=rendered_points
    ).strip()