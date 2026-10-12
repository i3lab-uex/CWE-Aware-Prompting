import html

# Template for rendering a user post.
# Placeholders: {username}, {post_title}, {post_body}, {tags}
USER_POST_FORMAT = (
    '<article class="user-post">\n'
    '  <header>\n'
    '    <h2>{post_title}</h2>\n'
    '    <p class="author">Posted by: {username}</p>\n'
    '  </header>\n'
    '  <div class="content">{post_body}</div>\n'
    '  <footer>{tags}</footer>\n'
    '</article>'
)

def render_user_post(username: str, post_title: str, post_body: str, tags: list[str]) -> str:
    """
    Render a user-generated forum post safely.

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
    """
    # Escape user supplied strings to prevent XSS (CWE-79)
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve line breaks; escape tags

    # Render each tag as a <span> element, escaping the tag text
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    )

    # Format the final HTML using a safe template
    rendered = USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body.replace('\n', '<br>'),
        tags=safe_tags
    )

    return rendered