import html

# Predefined HTML template with placeholders.
# Example: "<article><h2>{heading}</h2><p>by {poster}</p><div>{body}</div><footer>{labels}</footer></article>"
USER_POST_FORMAT = (
    "<article class=\"forum-post\">"
    "  <h2>{heading}</h2>"
    "  <p class=\"author\">by {poster}</p>"
    "  <div class=\"content\">{body}</div>"
    "  <footer class=\"tags\">{labels}</footer>"
    "</article>"
)

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
        List of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering.
    """
    # Escape all user-provided strings to prevent XSS and injection attacks
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)

    # The body may contain formatting; escape it and preserve newlines as <br>
    safe_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Convert each label to a <span> element, escaping its content
    safe_labels = "".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=safe_labels
    )