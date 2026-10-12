import html
from typing import List

# Example template; in real usage this would be defined elsewhere
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def create_forum_post(topic: str, text_body: str, points: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : list[str]
        A collection of user‑provided discussion points or options in markdown
        format. Each point will be escaped and rendered as a list item.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the title,
        body, and discussion points.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    # Basic type checks
    if not isinstance(topic, str):
        raise ValueError("topic must be a string")
    if not isinstance(text_body, str):
        raise ValueError("text_body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise ValueError("points must be a list of strings")

    # Escape user supplied content to avoid XSS
    escaped_title = html.escape(topic)
    escaped_body = html.escape(text_body)

    # Convert each point to an <li> element, escaping content
    escaped_points = "\n".join(f"<li>{html.escape(p)}</li>" for p in points)

    # Render the template
    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=escaped_points
    )