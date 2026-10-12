import html
from typing import List

# Example template (should be defined elsewhere in the real application)
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{heading}</h2>
  <p><strong>Author:</strong> {poster}</p>
  <div class="post-body">{body}</div>
  <div class="post-tags">
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
    labels : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string containing the formatted post.
    """
    # Escape user-provided content to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain line breaks but no quotes

    # Create span tags for each label, escaping label text
    safe_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>' for label in labels
    )

    # Format the final HTML using the template
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body.replace("\n", "<br>"),  # preserve line breaks
        labels=safe_labels,
    )