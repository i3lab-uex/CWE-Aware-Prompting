import html
from typing import List

# Predefined template for the forum post.
# Expected placeholders: {header}, {body}, {options}
FORUM_POST_FORMAT = """<h2>{header}</h2>
<div class="post-body">{body}</div>
{options}"""

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post.

    Args:
        title: The title or subject line of the forum post.
        body:  The main content or body of the forum post.
        topics: A list of discussion points in markdown format.

    Returns:
        A string containing the sanitized and formatted forum post, with
        options rendered as an HTML unordered list.
    """
    # Sanitize title and body to avoid XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Convert each topic to a list item, escaping any HTML characters.
    safe_items = []
    for t in topics:
        # Escape markdown special characters that could be interpreted as HTML
        escaped = html.escape(t, quote=True)
        safe_items.append(f"<li>{escaped}</li>")

    # Build the unordered list if there are topics
    options_html = ""
    if safe_items:
        options_html = "<ul>\n" + "\n".join(safe_items) + "\n</ul>"

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )