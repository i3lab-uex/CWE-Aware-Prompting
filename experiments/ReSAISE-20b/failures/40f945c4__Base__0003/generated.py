import html

# Predefined HTML template for a user post.
# Placeholders: {user_name}, {post_heading}, {post_content}, {post_tags}
USER_POST_FORMAT = """
<div class="user-post">
    <h2>{post_heading}</h2>
    <p class="author">by {user_name}</p>
    <div class="content">{post_content}</div>
    <div class="tags">
        {post_tags}
    </div>
</div>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a user's post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        Title of the user's post.
    post_content : str
        Main content of the user's post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing the sanitized HTML representation of the user's post.
    """
    # Escape user-controllable input to prevent XSS (CWE-79)
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(post_content, quote=False)  # Preserve line breaks

    # Build tags: each tag is wrapped in a <span> element
    safe_tags = ""
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags += f'<span class="tag">{escaped_tag}</span> '

    # Trim trailing space and insert into template
    safe_tags = safe_tags.strip()

    return USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_heading,
        post_content=safe_content,
        post_tags=safe_tags
    )