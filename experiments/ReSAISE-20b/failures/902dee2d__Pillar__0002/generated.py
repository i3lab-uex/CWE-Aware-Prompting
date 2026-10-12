import html
from typing import List

# Predefined HTML template for forum posts.
# Placeholders: {title}, {body}, {discussion}
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">{discussion}</ul>
</div>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a sanitized forum post from user‑provided content.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post.
    items : List[str]
        A series of discussion points or options in Markdown format.

    Returns
    -------
    str
        Fully formatted and sanitized HTML string ready for rendering.
    """
    # Sanitize the headline and content to avoid XSS or broken HTML
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Convert each markdown item into a safe <li> element
    safe_items = []
    for item in items:
        # Escape the markdown content to prevent injection
        escaped_item = html.escape(item, quote=True)
        # Basic Markdown → HTML conversion for emphasis and links
        # (very minimal; can be extended if needed)
        escaped_item = escaped_item.replace("**", "<b>").replace("*", "<i>")
        escaped_item = escaped_item.replace("[", "<a href='").replace("](", "'>") + "</a>"
        safe_items.append(f"<li>{escaped_item}</li>")

    discussion_html = "\n".join(safe_items)

    # Render the final HTML using the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_headline,
        body=safe_content,
        discussion=discussion_html
    )

    return formatted_post.strip()