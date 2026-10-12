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
        Author of the post.
    heading : str
        Title of the user's post.
    body : str
        Main content of the user's post.
    labels : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string representing the forum post.
    """
    # Escape all user-supplied strings to prevent XSS or injection
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)  # preserve newlines and indentation

    # Build tags string: each tag wrapped in a <span>
    safe_labels = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in labels
    )

    # Format the template with sanitized components
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=safe_labels
    )