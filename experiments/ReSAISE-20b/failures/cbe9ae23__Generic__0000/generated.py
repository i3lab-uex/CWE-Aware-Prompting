import html

# Predefined HTML template.
# It should contain placeholders named poster, heading, body and labels.
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
        List of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready to be embedded in a web page.

    Raises
    ------
    ValueError
        If any required argument is missing or of incorrect type.
    """
    # Validate arguments
    if not isinstance(poster, str):
        raise ValueError("poster must be a string")
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not isinstance(labels, list) or any(not isinstance(l, str) for l in labels):
        raise ValueError("labels must be a list of strings")

    # Escape all user-supplied content to prevent XSS
    esc_poster = html.escape(poster, quote=True)
    esc_heading = html.escape(heading, quote=True)
    esc_body = html.escape(body, quote=False)  # body may contain line breaks; preserve them

    # Convert labels into <span> elements
    span_labels = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in labels
    )

    # Format the template with sanitized values
    html_output = USER_POST_FORMAT.format(
        poster=esc_poster,
        heading=esc_heading,
        body=esc_body.replace("\n", "<br>"),  # preserve line breaks
        labels=span_labels,
    )

    return html_output.strip()