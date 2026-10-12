import html
from typing import List

# Example template – replace with the actual format used by your forum system.
FORUM_POST_FORMAT = """
<h1>{title}</h1>
<div class="post-body">{body}</div>
<ul class="discussion-points">
{points}
</ul>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given title, body and discussion points.

    Parameters
    ----------
    title : str
        The main topic or heading of the forum post.
    body : str
        The primary content of the post. May contain user‑supplied text.
    points : List[str]
        A list of discussion items in markdown format. Each item is rendered
        as a single <li> element.

    Returns
    -------
    str
        A fully formatted HTML string ready for rendering in the forum.
    """
    # Escape user supplied text to avoid XSS or malformed HTML
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert markdown discussion points into <li> tags.
    # We keep the markdown syntax but escape any HTML that might be present
    # to prevent injection. If you need full markdown rendering, replace this
    # with a proper markdown parser that escapes dangerous content.
    safe_points = []
    for point in points:
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"    <li>{escaped_point}</li>")

    points_html = "\n".join(safe_points)

    # Render the final template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return formatted_post.strip()