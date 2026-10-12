import html
from typing import List

# Example template; replace with the actual one if different.
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{heading}</h2>
  <p class="author">Posted by: {poster}</p>
  <div class="content">{body}</div>
  <div class="tags">{labels_html}</div>
</div>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    poster : str
        Author name.
    heading : str
        Post title.
    body : str
        Main content of the post.
    labels : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A string containing the sanitized HTML of the forum post.
    """
    # Escape user-provided content to prevent XSS
    escaped_poster = html.escape(poster, quote=True)
    escaped_heading = html.escape(heading, quote=True)
    escaped_body = html.escape(body, quote=False)  # preserve line breaks if needed

    # Build labels HTML
    escaped_labels = [f'<span class="tag">{html.escape(label, quote=True)}</span>' for label in labels]
    labels_html = ' '.join(escaped_labels)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster=escaped_poster,
        heading=escaped_heading,
        body=escaped_body,
        labels_html=labels_html
    )