import html
from typing import List

# Example template; in a real application this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p><strong>Author:</strong> {user_name}</p>
  <div class="content">{post_content}</div>
  <div class="tags">{post_tags}</div>
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

    Args:
        user_name: Author of the post.
        post_heading: Title of the post.
        post_content: Main content of the post.
        post_tags: List of tags associated with the post.

    Returns:
        A string containing sanitized HTML for the post.
    """
    # Escape all user-provided strings to prevent XSS
    safe_user_name = html.escape(user_name, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)

    # For content we allow line breaks but still escape HTML
    safe_post_content = html.escape(post_content, quote=True).replace("\n", "<br>")

    # Build tag spans
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_post_heading,
        post_content=safe_post_content,
        post_tags=tags_html
    )