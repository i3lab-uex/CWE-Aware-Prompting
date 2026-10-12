import html

# Example template (should be defined elsewhere in your code base)
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul>{discussion_points}</ul>
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Args:
        topic_title (str): The title or main topic of the forum post.
        body_text (str): The main body or content of the forum post.
        list_items (list[str]): A collection of discussion points in markdown format.

    Returns:
        str: Fully formatted and sanitized HTML string.
    """
    # Sanitize the title and body to prevent XSS
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Convert markdown discussion points to list items
    safe_items = []
    for item in list_items:
        # Escape each item and wrap it in <li>
        safe_item = html.escape(item, quote=True)
        safe_items.append(f"<li>{safe_item}</li>")
    discussion_html = "\n".join(safe_items)

    # Use the template to assemble the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion_points=discussion_html
    )