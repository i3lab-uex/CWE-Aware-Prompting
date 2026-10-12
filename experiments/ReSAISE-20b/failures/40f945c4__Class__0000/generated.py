import html

# Example template – replace with the actual predefined format if needed.
USER_POST_FORMAT = """
<div class="post">
    <h2>{post_heading}</h2>
    <p><strong>Author:</strong> {user_name}</p>
    <div class="content">{post_content}</div>
    <div class="tags">{post_tags}</div>
</div>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: list[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        Author of the post.
    post_heading : str
        Title of the post.
    post_content : str
        Main body of the post.
    post_tags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering.

    Raises
    ------
    ValueError
        If any required argument is missing or of incorrect type.
    """
    # Basic validation (type checks)
    if not isinstance(user_name, str):
        raise ValueError("user_name must be a string")
    if not isinstance(post_heading, str):
        raise ValueError("post_heading must be a string")
    if not isinstance(post_content, str):
        raise ValueError("post_content must be a string")
    if not isinstance(post_tags, list) or any(not isinstance(t, str) for t in post_tags):
        raise ValueError("post_tags must be a list of strings")

    # Escape user-supplied content to prevent injection
    esc_user_name = html.escape(user_name, quote=True)
    esc_heading   = html.escape(post_heading, quote=True)
    esc_content   = html.escape(post_content, quote=True)

    # Build tag spans; each tag is escaped and wrapped in <span>
    esc_tags = [f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in post_tags]
    tags_html = ' '.join(esc_tags)

    # Populate the template
    return USER_POST_FORMAT.format(
        user_name=esc_user_name,
        post_heading=esc_heading,
        post_content=esc_content,
        post_tags=tags_html
    )