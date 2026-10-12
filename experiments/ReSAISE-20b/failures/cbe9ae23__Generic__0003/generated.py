import html
from typing import List

# Predefined template for a forum post.
USER_POST_FORMAT = """
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

    Args:
        poster (str): Author of the post.
        heading (str): Title of the post.
        body (str): Main content of the post.
        labels (List[str]): List of tags associated with the post.

    Returns:
        str: Sanitized HTML string representing the forum post.
    """
    # Escape user-supplied text to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build tag spans, escaping each label
    safe_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        heading=safe_heading,
        poster=safe_poster,
        body=safe_body,
        labels=safe_labels
    )