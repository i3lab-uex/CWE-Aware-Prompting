import html
from typing import List

# Predefined HTML template with placeholders for poster, heading, body and labels
USER_POST_FORMAT: str = """
<div class="forum-post">
    <h2>{heading}</h2>
    <p class="author">Posted by: {poster}</p>
    <div class="content">{body}</div>
    <div class="tags">{labels}</div>
</div>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    poster : str
        Author of the post.
    heading : str
        Title of the post.
    body : str
        Main content of the post.
    labels : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a browser.
    """
    # Sanitize text fields to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)

    # The body might contain line breaks; preserve them with <br>
    safe_body = html.escape(body, quote=True).replace('\n', '<br>')

    # Convert tags into <span class="tag"> elements
    safe_labels = []
    for tag in labels:
        escaped_tag = html.escape(tag, quote=True)
        safe_labels.append(f'<span class="tag">{escaped_tag}</span>')
    labels_html = ' '.join(safe_labels)

    # Render the template
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=labels_html
    )