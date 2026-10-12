import html
from typing import List

# Template for a user post.  Placeholders are named for clarity.
USER_POST_FORMAT = """
<div class="post">
    <h2>{post_title}</h2>
    <p class="author">Posted by: {username}</p>
    <div class="body">{post_body}</div>
    <div class="tags">
        {tags}
    </div>
</div>
"""

def render_user_post(
    username: str,
    post_title: str,
    post_body: str,
    tags: List[str]
) -> str:
    """
    Render a user-generated post as sanitized HTML.

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
        A sanitized HTML representation of the post.
    """
    # Escape all user-provided data to prevent XSS (CWE-79)
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # body may contain newlines but not HTML

    # Render tags as <span> elements, escaping each tag value
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    )

    # Format the final HTML using the template
    rendered = USER_POST_FORMAT.format(
        post_title=safe_title,
        username=safe_username,
        post_body=safe_body,
        tags=safe_tags
    )
    return rendered.strip()