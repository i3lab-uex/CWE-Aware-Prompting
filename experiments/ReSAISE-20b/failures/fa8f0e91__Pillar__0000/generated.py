import html
from typing import List

# Template for rendering a user post. Placeholders:
# {username}, {post_title}, {post_body}, {tags}
USER_POST_FORMAT = """
<div class="user-post">
  <h2>{post_title}</h2>
  <p class="author">Posted by: {username}</p>
  <div class="content">{post_body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def render_user_post(username: str,
                     post_title: str,
                     post_body: str,
                     tags: List[str]) -> str:
    """
    Render a sanitized HTML representation of a user-generated post.

    Args:
        username: Name of the user who created the post.
        post_title: Title of the post.
        post_body: Main content of the post.
        tags: List of tag strings.

    Returns:
        A string containing well‑formed HTML with escaped user input.
    """
    # Escape all user-supplied data to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_title   = html.escape(post_title, quote=True)
    safe_body    = html.escape(post_body, quote=True)

    # Render tags as <span> elements; escape each tag individually
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    )

    # Format the final HTML using the template
    rendered = USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags=safe_tags
    )

    # Strip leading/trailing whitespace for a clean output
    return rendered.strip()