import html
from typing import List

# Example template (you can replace this with the actual predefined one)
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">Posted by: {user_name}</p>
  <div class="content">{post_content}</div>
  <div class="tags">{post_tags}</div>
</div>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        user_name: Author of the post.
        post_heading: Title of the post.
        post_content: Main body content of the post.
        post_tags: List of tags associated with the post.

    Returns:
        A string containing safe HTML for rendering the post.
    """
    # Sanitize all user-provided strings
    esc_user_name = html.escape(user_name, quote=True)
    esc_heading   = html.escape(post_heading, quote=True)
    esc_content   = html.escape(post_content, quote=True)

    # Build tag spans; each tag is escaped and wrapped in a <span>
    esc_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = ' '.join(esc_tags)

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        user_name=esc_user_name,
        post_heading=esc_heading,
        post_content=esc_content,
        post_tags=tags_html
    )