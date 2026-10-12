import html
from typing import List

# Predefined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be replaced
# with the sanitized values supplied by the caller.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def create_forum_post(topic: str, text_body: str, points: List[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : List[str]
        A collection of discussion points provided by users. Each point
        may contain Markdown or other user input.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string that can be safely
        embedded in a web page.

    Notes
    -----
    * All user input is escaped using :func:`html.escape` to neutralise
      any HTML or script injection attempts (CWE‑74).
    * The function does **not** perform Markdown rendering; it simply
      escapes the input and wraps each point in a <li> element.
    """
    # Escape all user supplied data to avoid injection attacks
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Build the <ul> with escaped list items
    if points:
        safe_points = ["<li>{}</li>".format(html.escape(p, quote=True)) for p in points]
        points_html = "<ul>\n" + "\n".join(safe_points) + "\n</ul>"
    else:
        points_html = ""

    # Substitute into the template
    return FORUM_POST_FORMAT.format(title=safe_title, body=safe_body, points=points_html)