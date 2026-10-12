import html

# Predefined HTML template with placeholders for poster, heading, body and labels.
USER_POST_FORMAT = """
<div class="forum-post">
    <h2>{heading}</h2>
    <p class="author">Posted by: {poster}</p>
    <div class="content">{body}</div>
    <div class="tags">{labels}</div>
</div>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        poster (str): Author of the post.
        heading (str): Title of the post.
        body (str): Main content of the post.
        labels (list[str]): List of tags associated with the post.

    Returns:
        str: Sanitized HTML string ready for inclusion in a web page.
    """
    # Escape user-provided content to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain <p> etc. but we still escape

    # Convert labels into sanitized <span> elements
    safe_labels = []
    for label in labels:
        escaped_label = html.escape(label, quote=True)
        safe_labels.append(f'<span class="tag">{escaped_label}</span>')
    labels_html = ' '.join(safe_labels)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        heading=safe_heading,
        poster=safe_poster,
        body=safe_body,
        labels=labels_html
    )