import html
from typing import List

# Predefined HTML template with placeholders
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{heading}</h2>
  <p class="author">Posted by: {poster}</p>
  <div class="content">{body}</div>
  <div class="tags">
    {labels}
  </div>
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
    labels : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string of the post.
    """
    # Escape user-provided content to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)

    # Convert labels to <span> elements
    safe_labels = []
    for label in labels:
        escaped_label = html.escape(label, quote=True)
        safe_labels.append(f'<span class="tag">{escaped_label}</span>')
    labels_html = ' '.join(safe_labels)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=labels_html
    )