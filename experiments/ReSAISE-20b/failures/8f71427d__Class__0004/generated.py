import html

# Example template; replace with the actual format used by your application.
USER_POST_FORMAT = (
    "<div class=\"post\">"
    "  <h1>{title}</h1>"
    "  <p class=\"author\">Posted by {username}</p>"
    "  <div class=\"body\">{body}</div>"
    "  {tags}"
    "</div>"
)

def render_user_content(username_key: str,
                        title_key: str,
                        body_key: str,
                        tag_elements: list[str]) -> str:
    """
    Generate a safe HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        The heading of the user's post.
    body_key : str
        The primary content of the user's post.
    tag_elements : list[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string representing the forum post.
    """
    # Basic validation of input types
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
            raise TypeError("Each tag must be a string")

    # Escape user supplied content to neutralize any HTML or script injection
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=True)

    # Build the tags section; each tag is wrapped in a <span>
    safe_tags = ""
    if tag_elements:
        span_parts = [f'<span class="tag">{html.escape(tag, quote=True)}</span>'
                      for tag in tag_elements]
        safe_tags = "".join(span_parts)

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )