import html
from typing import List

# Example forum post format template.
# The placeholders `{title}`, `{body}` and `{points}` will be replaced with the
# sanitized values below.
FORUM_POST_FORMAT: str = (
    "<div class=\"forum-post\">\n"
    "  <h2>{title}</h2>\n"
    "  <p>{body}</p>\n"
    "{points}\n"
    "</div>"
)

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str]
) -> str:
    """
    Build a safe HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : List[str]
        A list of discussion points. Each item may contain markdown but
        will be rendered as plain text inside a `<ul>` list.

    Returns
    -------
    str
        The fully formatted and sanitized HTML string ready to be served.

    Notes
    -----
    All user-supplied input is escaped using :func:`html.escape` to prevent
    cross‑site scripting (CWE-79). The bullet points are rendered as plain text
    within `<li>` tags; no markdown parsing is performed to avoid executing
    unintended HTML.
    """
    # Escape the title and body.  The newline characters are preserved
    # because they are safe in HTML text nodes.
    escaped_title = html.escape(post_title, quote=True)
    escaped_body = html.escape(post_body, quote=True)

    # Build the unordered list of discussion points.
    if bullet_points:
        escaped_items = [
            f"  <li>{html.escape(point, quote=True)}</li>"
            for point in bullet_points
        ]
        points_html = "<ul>\n" + "\n".join(escaped_items) + "\n</ul>"
    else:
        points_html = ""

    # Insert the escaped parts into the template.
    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=points_html
    )