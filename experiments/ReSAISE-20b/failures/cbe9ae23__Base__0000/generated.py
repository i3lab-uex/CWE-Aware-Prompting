import html

# Predefined HTML template with placeholders for poster, heading, body and labels.
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

def create_forum_post(poster: str, heading: str, body: str, labels: list[str]) -> str:
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
        List of tags.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering.
    """
    # Escape all user-provided content to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)

    # Escape each label and wrap in <span> tags
    escaped_labels = [f'<span class="tag">{html.escape(label, quote=True)}</span>' for label in labels]
    safe_labels = " ".join(escaped_labels)

    # Format the template with sanitized values
    return USER_POST_FORMAT.format(
        heading=safe_heading,
        poster=safe_poster,
        body=safe_body,
        labels=safe_labels
    )