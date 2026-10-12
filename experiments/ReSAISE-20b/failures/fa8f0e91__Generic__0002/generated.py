import html
from typing import List

# Template for rendering a user post.
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
    Render a user-generated post into safe HTML.

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
        Sanitized HTML string representing the post.
    """
    # Escape all user-supplied strings to prevent XSS
    esc_username = html.escape(username, quote=True)
    esc_title = html.escape(post_title, quote=True)
    esc_body = html.escape(post_body, quote=False)  # preserve line breaks

    # Render tags as <span> elements
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    ]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML using the template
    rendered = USER_POST_FORMAT.format(
        username=esc_username,
        post_title=esc_title,
        post_body=esc_body,
        tags_html=tags_html
    )

    return rendered.strip()