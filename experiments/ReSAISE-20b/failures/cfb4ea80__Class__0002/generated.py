import html
from typing import List

# Example template. In real usage this should be defined elsewhere.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">{points}</ul>
</div>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given title, body and discussion points.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML forum post.
    """
    # Escape all user‑supplied content to avoid injection (CWE-74)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each point to a sanitized <li> element
    safe_points = [
        f"<li>{html.escape(point, quote=True)}</li>" for point in points
    ]
    points_html = "\n".join(safe_points)

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )