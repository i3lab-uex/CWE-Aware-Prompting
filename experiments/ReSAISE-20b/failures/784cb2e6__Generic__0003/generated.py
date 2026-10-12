import html

# Predefined template for forum posts.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options}
"""

def create_forum_post(title: str, body: str, topics: list[str]) -> str:
    """
    Construct a forum post with a header, body and an HTML unordered list of topics.

    Args:
        title: The title or subject line of the forum post.
        body: The main content or body of the forum post.
        topics: A list of user‑provided options or discussion points.

    Returns:
        A string containing the sanitized and formatted forum post.
    """
    # Sanitize title and body to prevent XSS attacks.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert topics to an HTML unordered list.
    if topics:
        li_items = []
        for topic in topics:
            # Each topic may contain Markdown; escape HTML and keep basic formatting.
            escaped_topic = html.escape(topic, quote=True)
            li_items.append(f"<li>{escaped_topic}</li>")
        options_html = "<ul>\n" + "\n".join(li_items) + "\n</ul>"
    else:
        options_html = ""  # No topics provided.

    # Render the final post using the template.
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    ).strip()