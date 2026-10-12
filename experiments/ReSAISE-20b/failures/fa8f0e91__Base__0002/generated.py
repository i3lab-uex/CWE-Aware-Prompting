import html

# Template for rendering a user post.
USER_POST_FORMAT = """
<div class="user-post">
    <h2>{post_title}</h2>
    <p class="author">Posted by: {username}</p>
    <div class="body">{post_body}</div>
    <div class="tags">{tags_html}</div>
</div>
"""

def render_user_post(username: str, post_title: str, post_body: str, tags: list[str]) -> str:
    """
    Render a user-generated forum post as safe HTML.

    Parameters
    ----------
    username : str
        Name of the user who created the post.
    post_title : str
        Title of the post.
    post_body : str
        Main content of the post.
    tags : list[str]
        List of tags added by the user.

    Returns
    -------
    str
        A sanitized HTML string containing the post information.
    """
    # Escape all user-provided content to avoid XSS
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve line breaks but escape markup

    # Build safe tags
    tag_spans = []
    for t in tags:
        escaped_tag = html.escape(t, quote=True)
        tag_spans.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = ' '.join(tag_spans)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        post_title=safe_title,
        username=safe_username,
        post_body=safe_body,
        tags_html=tags_html
    )