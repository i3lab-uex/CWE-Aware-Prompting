import html
from typing import List

# Example template; in real use this would be defined elsewhere.
FORUM_POST_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <div class="post-content">
        {content}
    </div>
    <h2>Discussion Points</h2>
    <ul class="discussion-list">
        {items}
    </ul>
</body>
</html>
"""

def _markdown_to_ul(items: List[str]) -> str:
    """
    Convert a list of markdown items into an HTML unordered list.
    Each item is escaped to prevent injection.
    """
    li_elements = []
    for item in items:
        # Basic support: strip leading markdown bullet or number.
        cleaned = item.lstrip("-+*0123456789. ").strip()
        escaped = html.escape(cleaned)
        li_elements.append(f"<li>{escaped}</li>")
    return "\n".join(li_elements)

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the given headline, content and discussion points.

    Args:
        headline: The title of the forum post.
        content: The body text of the forum post.
        items: A list of discussion points in markdown format.

    Returns:
        A fully formatted and sanitized HTML string ready for rendering.
    """
    # Escape headline and content to avoid XSS or markup injection
    safe_headline = html.escape(headline)
    safe_content = html.escape(content).replace("\n", "<br>")

    # Convert discussion items to HTML list
    safe_items = _markdown_to_ul(items)

    # Format the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_headline,
        content=safe_content,
        items=safe_items
    )