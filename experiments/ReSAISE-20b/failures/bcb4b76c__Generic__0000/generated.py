import html
from typing import List

# Example template – in real use this should be defined elsewhere and imported.
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
        The main body/content of the forum post.
    points : List[str]
        A list of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    ValueError
        If any point string contains disallowed characters that could break HTML structure.

    Notes
    -----
    The function uses :func:`html.escape` to neutralise any potential XSS payloads.
    """
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")
    if not isinstance(text_body, str):
        raise TypeError("text_body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise TypeError("points must be a list of strings")

    # Escape title and body
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Build the list items for discussion points
    safe_points_items = []
    for point in points:
        # Basic validation: disallow raw < or > characters to prevent malformed tags
        if '<' in point or '>' in point:
            raise ValueError("Discussion points must not contain raw '<' or '>' characters.")
        safe_point = html.escape(point, quote=True)
        safe_points_items.append(f"<li>{safe_point}</li>")

    safe_points_html = "\n".join(safe_points_items)

    # Format the final HTML using the template
    formatted_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points_html
    )

    return formatted_html.strip()