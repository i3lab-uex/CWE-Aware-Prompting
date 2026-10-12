import html

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{heading}</h2>
  <p><strong>Posted by:</strong> {poster}</p>
  <div class="post-body">{body}</div>
  <div class="tags">
    {labels}
  </div>
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
        str: Sanitized HTML string representing the forum post.
    """
    # Escape all user-supplied content to prevent XSS / injection attacks
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=True)

    # Build the tags HTML
    tag_spans = []
    for tag in labels:
        safe_tag = html.escape(tag, quote=True)
        tag_spans.append(f'<span class="tag">{safe_tag}</span>')
    labels_html = ' '.join(tag_spans)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=labels_html
    )