import html
from typing import List

# Pre‑defined template for the forum post.  It contains three placeholders
# that will be replaced by the title, body content and discussion points.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  <div class="discussion-points">{points}</div>
</div>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    headline : str
        The title of the post.
    content : str
        The main body text of the post.
    items : list[str]
        Discussion points or options.  Each item may contain markdown syntax
        but is rendered as plain text inside an HTML list.

    Returns
    -------
    str
        A fully formatted forum post string that is safe for HTML output.

    Raises
    ------
    TypeError
        If any argument has an unexpected type.
    """
    # Validate input types
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not (isinstance(items, list) and all(isinstance(i, str) for i in items)):
        raise TypeError("items must be a list of strings")

    # Escape HTML special characters to prevent injection
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Render discussion points as an unordered list
    if items:
        safe_items = "".join(
            f"<li>{html.escape(item, quote=True)}</li>" for item in items
        )
        safe_points = f"<ul>{safe_items}</ul>"
    else:
        # If no items are provided, omit the section
        safe_points = ""

    # Construct final HTML using the template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return post_html.strip()