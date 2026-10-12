import html
from typing import List

# Example forum post format. The placeholders {title}, {body} and {points}
# will be replaced by the function below. Feel free to modify this template
# as needed for your forum system.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a sanitized HTML forum post from the given title, body and discussion points.

    Parameters
    ----------
    title : str
        The forum post title.
    body : str
        The main content of the post. May contain line breaks.
    points : List[str]
        A list of discussion points/options, each represented as a markdown string.
        The function will render them as an unordered list.

    Returns
    -------
    str
        A fully formatted and HTML‑escaped forum post ready for display.

    Raises
    ------
    ValueError
        If any of the inputs are not of the expected type.
    """
    # Basic type checks
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise ValueError("points must be a list of strings")

    # Escape user input to prevent XSS
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Render discussion points as an unordered list
    if points:
        escaped_points = "\n".join(
            f"    <li>{html.escape(point, quote=True)}</li>" for point in points
        )
        points_html = f"\n<ul>\n{escaped_points}\n</ul>"
    else:
        points_html = ""

    # Substitute placeholders in the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=points_html
    )

    return formatted_post.strip()