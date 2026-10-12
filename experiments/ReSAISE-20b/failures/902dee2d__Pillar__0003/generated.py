import html
from typing import List

# Pre‑defined HTML template for forum posts.
# The placeholders {title}, {body} and {points} will be replaced by the function.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from user supplied data.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary content or body text of the post.
    items : list[str]
        A series of discussion points. Each point may contain markdown
        syntax but will be rendered as plain text within an unordered list.

    Returns
    -------
    str
        A fully formatted, sanitized HTML forum post.
    """
    # Validate inputs
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
        raise TypeError("items must be a list of strings")

    # Escape user input to prevent XSS and ensure well‑formedness.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Convert discussion points into a safe HTML unordered list.
    if items:
        escaped_items = [f"<li>{html.escape(item, quote=True)}</li>" for item in items]
        points_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        points_html = ""

    # Render the final HTML using the predefined format.
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )
    return post_html.strip()