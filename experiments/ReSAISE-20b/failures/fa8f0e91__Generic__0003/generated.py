import html

# Template for rendering a user post.
USER_POST_FORMAT = """
<div class="user-post">
  <h2>{post_title}</h2>
  <p class="body">{post_body}</p>
  <div class="meta">
    <span class="author">Posted by: {username}</span>
    <div class="tags">{tags_html}</div>
  </div>
</div>
"""

def render_user_post(username: str, post_title: str, post_body: str, tags: list[str]) -> str:
    """
    Render a user-generated forum post as safe HTML.

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
        Sanitized HTML string representing the post.
    """
    # Escape user supplied content to prevent XSS attacks
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve line breaks

    # Render tags as <span> elements
    safe_tags = [f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in tags]
    tags_html = ' '.join(safe_tags)

    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags_html=tags_html
    )