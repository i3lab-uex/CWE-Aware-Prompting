import html
from typing import List

# Template for rendering a user post. The placeholders will be replaced by the
# sanitized values.
USER_POST_FORMAT = """
<div class="user-post">
  <h2>{post_title}</h2>
  <p class="author">Posted by: {username}</p>
  <div class="content">{post_body}</div>
  <div class="tags">{tags_html}</div>
</div>
"""

def render_user_post(
    username: str,
    post_title: str,
    post_body: str,
    tags: List[str]
) -> str:
    """
    Render a user-generated post as safe HTML.

    Parameters
    ----------
    username : str
        The name of the user who created the post.
    post_title : str
        The title of the post.
    post_body : str
        The main content of the post.
    tags : List[str]
        A list of tags added by the user.

    Returns
    -------
    str
        Sanitized HTML containing the post information.
    """
    # Sanitize all user-provided strings to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)

    # Build the tags HTML
    safe_tags = [f'<span>{html.escape(tag, quote=True)}</span>' for tag in tags]
    tags_html = " ".join(safe_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags_html=tags_html
    )