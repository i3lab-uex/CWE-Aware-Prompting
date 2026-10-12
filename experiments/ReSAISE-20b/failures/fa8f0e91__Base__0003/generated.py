import html

# Template for rendering a user post.  The placeholders are:
#   {username}   – the author's name
#   {title}      – the post title
#   {body}       – the main content of the post
#   {tags}       – a string containing all tags wrapped in <span> elements
USER_POST_FORMAT = (
    '<article class="user-post">\n'
    '  <header>\n'
    '    <h2>{title}</h2>\n'
    '    <p class="author">Posted by: {username}</p>\n'
    '  </header>\n'
    '  <div class="content">{body}</div>\n'
    '  <footer>{tags}</footer>\n'
    '</article>'
)

def render_user_post(username: str, post_title: str,
                     post_body: str, tags: list[str]) -> str:
    """
    Render a user-generated post as sanitized HTML.

    Args:
        username: The name of the user who created the post.
        post_title: The title of the post.
        post_body: The main content of the post.
        tags: A list of tags added by the user.

    Returns:
        A string containing the HTML representation of the post with all
        user-provided content properly escaped to prevent XSS.

    Raises:
        TypeError: If any argument is not of the expected type.
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

    # Escape user input to neutralize HTML/JS injection
    esc_username = html.escape(username, quote=True)
    esc_title   = html.escape(post_title, quote=True)
    esc_body    = html.escape(post_body, quote=False)  # preserve newlines

    # Render tags as <span> elements
    escaped_tags = []
    for tag in tags:
        esc_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{esc_tag}</span>')
    tags_html = ' '.join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        username=esc_username,
        title=esc_title,
        body=esc_body.replace('\n', '<br>'),
        tags=tags_html
    )