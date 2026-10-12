import html
from typing import List

# Pre‑defined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    {discussion_points}
</div>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post with a title, body content, and discussion points.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post.
    items : List[str]
        A list of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post as an HTML string.
    """
    # Sanitize the headline and body to avoid XSS
    safe_headline = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Convert discussion points into an HTML unordered list
    if items:
        safe_items = [html.escape(item, quote=True) for item in items]
        discussion_html = (
            '<ul class="discussion-points">\n'
            + "\n".join(f"    <li>{item}</li>" for item in safe_items)
            + "\n</ul>"
        )
    else:
        discussion_html = ""

    # Render the final post using the template
    return FORUM_POST_FORMAT.format(
        title=safe_headline,
        body=safe_body,
        discussion_points=discussion_html
    )