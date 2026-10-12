import html
from typing import List

# A simple HTML template for forum posts.
# {title}, {body} and {points} are placeholders that will be substituted
# with the escaped content provided by the caller.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str]
) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : List[str]
        A collection of user‑provided discussion points or options in
        markdown format.  Each item is rendered as a list element.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the title,
        body, and discussion points.

    Notes
    -----
    * All user input is escaped using :func:`html.escape` to prevent
      cross‑site scripting (XSS) attacks.
    * The function does not interpret Markdown; it simply escapes the
      text and wraps each point in an `<li>` element.  If Markdown
      rendering is required, replace the escaping logic with a safe
      Markdown renderer that strips dangerous tags (e.g. `bleach`).
    """
    # Escape the title and body to neutralize any HTML that might be
    # injected by a malicious user.
    safe_title = html.escape(post_title, quote=True)
    safe_body  = html.escape(post_body, quote=True)

    # Build the list of discussion points. Each point is escaped
    # individually and then wrapped in a <li> element.
    if bullet_points:
        list_items = "\n".join(
            f"  <li>{html.escape(point, quote=True)}</li>"
            for point in bullet_points
        )
        points_html = f"\n<ul>\n{list_items}\n</ul>"
    else:
        points_html = ""

    # Substitute the escaped content into the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )