import html

# Template for a user post (placeholder names in {curly braces})
USER_POST_FORMAT = (
    '<div class="post">\n'
    '  <h2>{post_title}</h2>\n'
    '  <p class="author">Posted by: {username}</p>\n'
    '  <div class="content">{post_body}</div>\n'
    '  <p class="tags">Tags: {tags_html}</p>\n'
    '</div>'
)

def render_user_post(username: str, post_title: str, post_body: str, tags: list[str]) -> str:
    """
    Render a user-generated forum post safely for HTML output.

    Parameters
    ----------
    username : str
        The name of the user who created the post.
    post_title : str
        The title of the post.
    post_body : str
        The main content of the post.
    tags : list[str]
        A list of tags added by the user.

    Returns
    -------
    str
        A sanitized HTML string representing the post.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Validate input types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(post_title, str):
        raise TypeError("post_title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        raise TypeError("tags must be a list of strings")

    # Escape all user-supplied content to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)

    # Build tag spans
    tag_spans = []
    for t in tags:
        safe_tag = html.escape(t, quote=True)
        tag_spans.append(f'<span>{safe_tag}</span>')
    tags_html = ' '.join(tag_spans)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags_html=tags_html
    )