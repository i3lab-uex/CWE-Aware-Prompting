import html

# A minimal HTML template for a forum post.
# {poster}, {heading}, {body} are placeholders for the main content.
# {labels} will contain a series of <span> elements representing tags.
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
        Title of the post.
    body : str
        Main content of the post.
    labels : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.

    Raises
    ------
    TypeError
        If any of the arguments are not of the expected type.
    """
    # Validate argument types
    if not isinstance(poster, str):
        raise TypeError("poster must be a string")
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(labels, list) or not all(isinstance(l, str) for l in labels):
        raise TypeError("labels must be a list of strings")

    # Escape all user-supplied content to prevent XSS and injection.
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain line breaks

    # Build tag spans; each tag is escaped and wrapped in a <span>.
    safe_tags = ' '.join(f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in labels)

    # Format the final HTML string.
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body.replace('\n', '<br>'),  # preserve line breaks
        labels=safe_tags
    )