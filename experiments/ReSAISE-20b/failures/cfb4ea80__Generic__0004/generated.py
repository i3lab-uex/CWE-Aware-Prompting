import html
from typing import List

# Pre‑defined HTML template for a forum post.
# It contains placeholders `{title}`, `{body}` and `{points}` that will be replaced
# with the user supplied values. The placeholders are named to avoid accidental
# formatting by Python's `format` method.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a structured forum post from the given title, body and discussion points.

    Parameters
    ----------
    title : str
        The main topic or heading of the forum post.
    body : str
        Primary content of the post. May contain plain text or HTML markup,
        but any user supplied characters are escaped to prevent XSS.
    points : list[str]
        Discussion points or options. Each element is expected to be a Markdown
        string but will be converted to plain text and escaped.

    Returns
    -------
    str
        A fully formatted, safe HTML string ready for rendering on a web page.

    Notes
    -----
    - All user supplied content is escaped using `html.escape` to avoid cross‑site
      scripting attacks.
    - The points are rendered as an unordered list (`<ul>`). Empty lists produce
      no `<ul>`.
    """
    # Escape user supplied data to avoid injection of malicious HTML/JS.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert points to an HTML unordered list.
    if points:
        # Escape each point individually and wrap it in <li>.
        escaped_points = "".join(
            f"<li>{html.escape(p, quote=True)}</li>" for p in points
        )
        points_html = f"<ul>{escaped_points}</ul>"
    else:
        points_html = ""

    # Combine everything using the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )