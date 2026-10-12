import html

# Example template – replace with the actual one if different.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">by {user_name}</p>
  <div class="content">{post_content}</div>
  <div class="tags">{post_tags}</div>
</div>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        The title of the post.
    post_content : str
        The main body of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The HTML string ready for safe rendering.
    """
    # Escape all user-provided content to avoid injection
    esc_user_name = html.escape(user_name, quote=True)
    esc_heading   = html.escape(post_heading, quote=True)
    esc_content   = html.escape(post_content, quote=False)

    # Sanitize tags and wrap each in a <span>
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = ' '.join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        user_name=esc_user_name,
        post_heading=esc_heading,
        post_content=esc_content,
        post_tags=tags_html
    )