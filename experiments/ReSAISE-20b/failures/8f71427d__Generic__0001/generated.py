import html

# Example template; replace with the actual one if different.
USER_POST_FORMAT = (
    "<article>"
    "  <h1>{title}</h1>"
    "  <p><strong>Author:</strong> {username}</p>"
    "  <div>{body}</div>"
    "  <footer>{tags}</footer>"
    "</article>"
)

def render_user_content(username_key: str,
                        title_key: str,
                        body_key: str,
                        tag_elements: list[str]) -> str:
    """
    Generate a secure HTML representation of a user's forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        Heading of the user's post.
    body_key : str
        Primary content of the user's post.
    tag_elements : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the forum post.
    """
    # Escape all user supplied content to prevent XSS
    escaped_username = html.escape(username_key, quote=True)
    escaped_title = html.escape(title_key, quote=True)
    escaped_body = html.escape(body_key, quote=True)

    # Build tag spans
    escaped_tags = [
        f'<span>{html.escape(tag, quote=True)}</span>' for tag in tag_elements
    ]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        title=escaped_title,
        username=escaped_username,
        body=escaped_body,
        tags=tags_html
    )