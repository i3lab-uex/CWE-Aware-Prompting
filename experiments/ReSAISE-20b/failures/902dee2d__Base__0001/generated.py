import html
from typing import List

# Pre‑defined template for the forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {discussion}
</div>
"""

def _render_discussion_items(items: List[str]) -> str:
    """
    Convert a list of markdown items into an HTML unordered list.
    Each item is escaped to prevent XSS and then wrapped in <li>.
    """
    if not items:
        return ""
    escaped_items = [f"<li>{html.escape(item)}</li>" for item in items]
    return f"\n<ul>\n{''.join(escaped_items)}\n</ul>"

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the provided headline, content and discussion items.
    
    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary content or body text of the post.
    items : list[str]
        A series of user‑supplied discussion points or options in markdown format.
    
    Returns
    -------
    str
        A fully formatted, sanitized HTML string suitable for rendering on a web page.
    
    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
        raise TypeError("items must be a list of strings")

    # Escape user input to prevent XSS
    safe_title = html.escape(headline)
    safe_body = html.escape(content).replace("\n", "<br>")  # preserve line breaks

    discussion_html = _render_discussion_items(items)

    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion=discussion_html
    )