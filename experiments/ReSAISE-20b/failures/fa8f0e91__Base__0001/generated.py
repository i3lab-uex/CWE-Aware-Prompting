import html
from typing import List

# Template for rendering a user post. Placeholders are named for clarity.
USER_POST_FORMAT = """
<div class="user-post">
    <h2>{post_title}</h2>
    <p class="body">{post_body}</p>
    <div class="meta">
        <span class="author">Posted by: {username}</span>
    </div>
    <div class="tags">
        {tag_elements}
    </div>
</div>
"""

def render_user_post(username: str,
                     post_title: str,
                     post_body: str,
                     tags: List[str]) -> str:
    """
    Render a sanitized HTML representation of a user-generated post.

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
        A sanitized HTML string ready to be served to clients.
    """
    # Escape all user-controlled input to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the tag elements
    escaped_tags = [html.escape(tag, quote=True) for tag in tags]
    tag_elements = " ".join(f'<span class="tag">{t}</span>' for t in escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tag_elements=tag_elements
    )