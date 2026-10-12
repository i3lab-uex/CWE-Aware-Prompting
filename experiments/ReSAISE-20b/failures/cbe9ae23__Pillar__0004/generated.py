import html
from typing import List

# Predefined HTML template with placeholders for the post's components.
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

def create_forum_post(poster: str, heading: str, body: str, labels: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        poster (str): The author of the post.
        heading (str): The title of the user's post.
        body (str): The main content of the user's post.
        labels (List[str]): A list of tags associated with the post.

    Returns:
        str: The sanitized HTML string ready for rendering.

    Raises:
        ValueError: If any required argument is missing or not a string/list.
    """
    # Basic type validation
    if not isinstance(poster, str):
        raise ValueError("poster must be a string")
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not isinstance(labels, list) or any(not isinstance(l, str) for l in labels):
        raise ValueError("labels must be a list of strings")

    # Escape all user-supplied content to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain newlines

    # Render tags as <span> elements, escaping each tag value
    safe_labels = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in labels
    )

    # Format the final HTML string
    post_html = USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body.replace("\n", "<br>"),  # preserve line breaks
        labels=safe_labels,
    )

    return post_html.strip()