import html
from typing import List

# Template for a user post.  Placeholders are replaced using .format().
USER_POST_FORMAT = """
<div class="user-post">
    <h2>{post_title}</h2>
    <p>by <strong>{username}</strong></p>
    <div class="post-body">{post_body}</div>
    <div class="tags">{tags_html}</div>
</div>
"""

def render_user_post(username: str, post_title: str, post_body: str,
                     tags: List[str]) -> str:
    """
    Render a user-generated post safely for inclusion in HTML.

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
    # Escape all user-supplied content to prevent XSS / injection
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve line breaks

    # Escape tags individually and wrap them in <span>
    escaped_tags = [f'<span>{html.escape(tag, quote=True)}</span>' for tag in tags]
    tags_html = ' '.join(escaped_tags)

    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags_html=tags_html
    )