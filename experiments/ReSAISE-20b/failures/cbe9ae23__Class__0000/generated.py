import html

# Predefined HTML template for a forum post.
# The placeholders {poster}, {heading}, {body}, and {labels} will be replaced
# by the sanitized values passed to create_forum_post.
USER_POST_FORMAT: str = """
<div class="forum-post">
    <h2>{heading}</h2>
    <p class="author">Posted by: {poster}</p>
    <div class="content">{body}</div>
    <div class="tags">
        {labels}
    </div>
</div>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: list[str]) -> str:
    """
    Generate an HTML representation of a forum post.

    Args:
        poster: The author of the post.
        heading: The title of the user's post.
        body: The main content of the user's post.
        labels: A list of tags associated with the post.

    Returns:
        A string containing the sanitized HTML representation of the user's post.
    """
    # Sanitize all user supplied strings to prevent injection
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)

    # Convert the list of tags into <span> elements, each tag is escaped.
    safe_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the final HTML using the predefined template.
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=safe_labels
    )