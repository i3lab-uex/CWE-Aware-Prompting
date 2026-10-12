import html
from typing import List

# Example template – replace with the actual one used in your system.
FORUM_POST_FORMAT = """
<h1>{title}</h1>
<div class="post-body">{body}</div>
<ul class="discussion-points">
{points}
</ul>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a forum post from user‑supplied content.

    Parameters
    ----------
    title : str
        The forum post's title or main topic.
    body : str
        The primary content of the post.
    points : list[str]
        Discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post ready for display.
    """
    # Escape all user‑supplied strings to prevent HTML injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each point to an <li> element, escaping any special characters
    list_items = []
    for point in points:
        escaped_point = html.escape(point, quote=True)
        list_items.append(f"    <li>{escaped_point}</li>")
    safe_points = "\n".join(list_items)

    # Render the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )