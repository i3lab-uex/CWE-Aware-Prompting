import html
from typing import List

# Template for rendering a user post. The placeholders are named:
# {username}, {post_title}, {post_body} and {tags}
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
                     tags: List[str]) -> str:
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
    tags : list[str]
        A list of tags added by the user.

    Returns
    -------
    str
        Sanitized HTML representation of the post.
    """
    # Escape all user-supplied strings to avoid XSS and ensure well‑formed HTML.
    esc_username = html.escape(username, quote=True)
    esc_title = html.escape(post_title, quote=True)
    esc_body = html.escape(post_body, quote=True)

    # Build tag HTML: each tag wrapped in a <span> element.
    esc_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    )

    # Format the final HTML using the template.
    rendered = USER_POST_FORMAT.format(
        username=esc_username,
        post_title=esc_title,
        post_body=esc_body,
        tags=esc_tags
    )

    return rendered.strip()