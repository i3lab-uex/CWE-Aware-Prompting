import html

# Template for rendering a user post.
USER_POST_FORMAT = """
<div class="user-post">
  <h2>{post_title}</h2>
  <p>by <strong>{username}</strong></p>
  <div class="post-body">{post_body}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def render_user_post(username: str, post_title: str, post_body: str,
                     tags: list[str]) -> str:
    """
    Render a user-generated post into sanitized HTML.

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
        Sanitized HTML representation of the post.
    """
    # Sanitize all user-supplied text to prevent XSS attacks.
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve line breaks

    # Convert tags into <span> elements and escape each tag.
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    )

    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body.replace('\n', '<br>'),
        tags=safe_tags
    )