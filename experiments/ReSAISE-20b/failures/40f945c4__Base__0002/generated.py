import html
from typing import List

# Predefined template with placeholders for user, heading, content and tags
USER_POST_FORMAT: str = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">Posted by: {user_name}</p>
  <div class="content">{post_content}</div>
  <div class="tags">
    {post_tags}
  </div>
</div>
"""

def build_post_html(
    user_name: str,
    post_heading: str,
    post_content: str,
    post_tags: List[str]
) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        Author's name.
    post_heading : str
        Title of the post.
    post_content : str
        Main content of the post.
    post_tags : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready to be served.
    """
    # Escape all user-provided content to prevent XSS
    escaped_user_name = html.escape(user_name, quote=True)
    escaped_heading = html.escape(post_heading, quote=True)
    escaped_content = html.escape(post_content, quote=False)

    # Convert tags to <span> elements
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = ' '.join(escaped_tags)

    # Format the template with sanitized values
    return USER_POST_FORMAT.format(
        user_name=escaped_user_name,
        post_heading=escaped_heading,
        post_content=escaped_content,
        post_tags=tags_html
    )