import html
from typing import List

# Example format: adjust as needed for your application.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_title}</h2>
  <p>by {username}</p>
  <div class="body">{post_body}</div>
  <div class="tags">{tags_html}</div>
</div>
"""

def render_user_post(username: str,
                     post_title: str,
                     post_body: str,
                     tags: List[str]) -> str:
    """
    Render a user-generated post safely for display in HTML.

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
        An HTML string containing the sanitized post.
    """
    # Escape all user-supplied content to prevent XSS or injection
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # body may contain line breaks

    # Render tags as <span> elements, escaping each tag
    safe_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    ]
    tags_html = " ".join(safe_tags)

    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags_html=tags_html
    )