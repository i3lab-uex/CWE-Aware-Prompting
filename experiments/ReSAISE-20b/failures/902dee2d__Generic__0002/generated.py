import html
from typing import List

# Pre‑defined template with placeholders for title, content and discussion points.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-content">{body}</div>
  {discussion_section}
</div>
"""

def _sanitize(text: str) -> str:
    """
    Escape HTML special characters to prevent injection attacks.
    """
    return html.escape(text, quote=True)

def _build_discussion_list(items: List[str]) -> str:
    """
    Convert a list of markdown items into an HTML unordered list.
    Items are escaped to avoid XSS. Markdown syntax is not processed;
    if needed, a full markdown renderer could be used instead.
    """
    if not items:
        return ""
    list_items = "".join(f"<li>{_sanitize(item)}</li>" for item in items)
    return f"\n<ul>\n{list_items}\n</ul>"

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given components.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post.
    items : list[str]
        Discussion points or options to be rendered as an unordered list.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string ready for rendering.
    """
    # Sanitize user input
    safe_title = _sanitize(headline)
    safe_body = _sanitize(content)

    # Build discussion section
    discussion_section = _build_discussion_list(items)
    if discussion_section:
        discussion_html = f"<h3>Discussion Points</h3>\n{discussion_section}"
    else:
        discussion_html = ""

    # Render final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion_section=discussion_html
    )