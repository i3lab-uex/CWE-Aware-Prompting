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

    Parameters
    ----------
    poster : str
        The author of the post.
    heading : str
        The title of the user's post.
    body : str
        The main content of the user's post.
    labels : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string for the forum post.
    """
    # Escape all user-provided strings to prevent XSS attacks
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render each label as a <span> element
    safe_labels = "".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=safe_labels
    )