import html
from typing import List

# Predefined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    <ul>{discussion_points}</ul>
</div>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the given headline, content, and discussion points.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary content or body text of the post.
    items : list[str]
        A series of user-supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post, including the header,
        message body, and safely rendered discussion points.

    Notes
    -----
    All user-supplied input is HTML-escaped to prevent injection attacks.
    The markdown in `items` is treated as plain text; no Markdown-to-HTML
    conversion is performed to avoid accidental execution of HTML or scripts.
    """
    # Sanitize headline and content
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Convert discussion points into an HTML unordered list.
    # Each item is escaped and wrapped in <li> tags.
    safe_items = []
    for idx, point in enumerate(items):
        # Escape the point text
        escaped_point = html.escape(point, quote=True)
        safe_items.append(f'<li>{escaped_point}</li>')

    discussion_html = "\n".join(safe_items)

    # Populate the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_headline,
        body=safe_content,
        discussion_points=discussion_html
    )

    return formatted_post.strip()