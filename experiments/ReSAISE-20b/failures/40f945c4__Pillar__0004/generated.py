import html
from typing import List

# A simple HTML template for a forum post.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p><strong>Author:</strong> {user_name}</p>
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
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        Title of the post.
    post_content : str
        Main content of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A sanitized HTML string ready to be embedded in a page.
    """
    # Escape all user-supplied strings to avoid XSS.
    esc_user_name = html.escape(user_name, quote=True)
    esc_post_heading = html.escape(post_heading, quote=True)
    esc_post_content = html.escape(post_content, quote=False)

    # Render each tag as a <span> element. Escape the tag name.
    escaped_tags = []
    for tag in post_tags:
        esc_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{esc_tag}</span>')

    # Join tags with a space separator.
    tags_html = " ".join(escaped_tags)

    # Format the final HTML using the template.
    return USER_POST_FORMAT.format(
        user_name=esc_user_name,
        post_heading=esc_post_heading,
        post_content=esc_post_content,
        post_tags=tags_html
    )