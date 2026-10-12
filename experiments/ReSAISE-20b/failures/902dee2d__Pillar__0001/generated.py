import html
from typing import List

# Example template; in a real system this would be defined elsewhere.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  <ul class="discussion-points">
    {points}
  </ul>
</div>
"""

def _sanitize_markdown_item(item: str) -> str:
    """
    Convert a markdown string into safe HTML for list items.
    Only plain text is allowed; any markup is escaped to prevent XSS.
    """
    # Escape HTML special characters
    safe_text = html.escape(item, quote=True)
    # Convert markdown links to plain text (simple approach)
    # e.g. [text](url) -> text
    import re
    safe_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', safe_text)
    # Convert markdown emphasis to <em> tags
    safe_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', safe_text)
    return f"<li>{safe_text}</li>"

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the given headline, content, and discussion points.
    
    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post.
    items : List[str]
        A list of discussion points or options in markdown format.
    
    Returns
    -------
    str
        A fully formatted and sanitized forum post ready for rendering.
    
    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type or if the template is malformed.
    """
    # Basic type checks
    if not isinstance(headline, str):
        raise ValueError("headline must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
        raise ValueError("items must be a list of strings")

    # Escape title and body to avoid injection
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Build discussion points list
    if items:
        safe_points = "\n".join(_sanitize_markdown_item(item) for item in items)
    else:
        safe_points = ""  # No points, leave empty list

    try:
        post_html = FORUM_POST_FORMAT.format(
            title=safe_title,
            body=safe_body,
            points=safe_points
        )
    except KeyError as e:
        raise ValueError(f"Template placeholder missing: {e}") from e

    return post_html.strip()