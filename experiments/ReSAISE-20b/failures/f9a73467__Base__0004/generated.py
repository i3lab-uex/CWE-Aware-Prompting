import html
from typing import List

# Predefined HTML template for forum posts.  The placeholders are named to
# match the keyword arguments in `compile_post`.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {discussion}
</div>
"""

def _render_highlights(highlights: List[str]) -> str:
    """
    Convert a list of markdown discussion points into an HTML unordered list.
    The content is escaped to prevent XSS.
    """
    if not highlights:
        return ""

    # Escape each item and wrap it in <li>
    escaped_items = [f"<li>{html.escape(item)}</li>" for item in highlights]
    return f"<ul>\n{''.join(escaped_items)}\n</ul>"

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given components.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content/body of the post. May contain user-supplied
        markdown or plain text.
    highlights : List[str]
        A series of discussion points. These are rendered as an HTML
        unordered list.

    Returns
    -------
    str
        A fully formatted, sanitized forum post ready to be served in a web page.
    """
    # Escape title and body content.  We use html.escape to neutralize any
    # HTML tags or JavaScript that might be injected by a malicious user.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(text, quote=True)

    # Render discussion points as an unordered list.  The function itself
    # escapes each item.
    safe_discussion = _render_highlights(highlights)

    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion=safe_discussion
    )