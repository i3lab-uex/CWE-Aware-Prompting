import html

# Example template – adjust placeholders as needed for your environment.
USER_POST_FORMAT = (
    "<article class=\"post\">"
    "  <h2>{title}</h2>"
    "  <p class=\"author\">Posted by: {username}</p>"
    "  <div class=\"content\">{body}</div>"
    "  <footer class=\"tags\">{tags}</footer>"
    "</article>"
)

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: list[str],
) -> str:
    """
    Generate a safe HTML representation of a forum post.

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
        XSS‑protected HTML string ready for rendering.
    """
    # Escape all user-controllable data
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=False)  # Preserve line breaks/whitespace

    # Wrap each tag in a <span> after escaping
    safe_tags = []
    for tag in tag_elements:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = " ".join(safe_tags)

    # Render the final HTML using the template
    return USER_POST_FORMAT.format(
        title=safe_title,
        username=safe_username,
        body=safe_body,
        tags=tags_html
    )