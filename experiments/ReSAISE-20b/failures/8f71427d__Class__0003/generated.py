import html

# Predefined template with placeholders for username, title, body and tags.
USER_POST_FORMAT = (
    "<article class='post'>"
    "  <header>"
    "    <h2>{title}</h2>"
    "    <p class='author'>Posted by {username}</p>"
    "  </header>"
    "  <section class='content'>"
    "    {body}"
    "  </section>"
    "  <footer class='tags'>"
    "    {tag_elements}"
    "  </footer>"
    "</article>"
)

def render_user_content(username_key: str, title_key: str,
                        body_key: str, tag_elements: list[str]) -> str:
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
        XSS‑protected HTML version of the user's forum post.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    """
    # Basic type checking
    if not isinstance(username_key, str):
        raise TypeError("username_key must be a string")
    if not isinstance(title_key, str):
        raise TypeError("title_key must be a string")
    if not isinstance(body_key, str):
        raise TypeError("body_key must be a string")
    if not isinstance(tag_elements, list):
        raise TypeError("tag_elements must be a list of strings")
    for tag in tag_elements:
        if not isinstance(tag, str):
            raise TypeError("each tag must be a string")

    # Escape all user‑supplied content to neutralize special HTML characters
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)

    # The body may contain line breaks; preserve them by converting to <br>
    safe_body_lines = [html.escape(line, quote=True) for line in body_key.splitlines()]
    safe_body = "<br>".join(safe_body_lines)

    # Wrap each tag in a <span> and escape it
    safe_tags = " ".join(f"<span class='tag'>{html.escape(tag, quote=True)}</span>"
                         for tag in tag_elements)

    # Format the final HTML using the safe components
    rendered_html = USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tag_elements=safe_tags
    )

    return rendered_html