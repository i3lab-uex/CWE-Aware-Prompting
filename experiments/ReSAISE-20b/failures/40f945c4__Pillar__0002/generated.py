import html
from typing import List

# Predefined HTML template with placeholders for user_name, post_heading,
# post_content and a placeholder that will be replaced by rendered tags.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">Posted by: {user_name}</p>
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

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        The title of the user's post.
    post_content : str
        The main content of the user's post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string for the post.
    """
    # Escape all user supplied content to avoid XSS
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(post_content)

    # Render tags as separate <span> elements
    rendered_tags = ""
    for tag in post_tags:
        safe_tag = html.escape(tag, quote=True)
        rendered_tags += f'<span class="tag">{safe_tag}</span> '

    # Strip trailing space
    rendered_tags = rendered_tags.rstrip()

    # Format the final HTML using the template
    html_output = USER_POST_FORMAT.format(
        post_heading=safe_heading,
        user_name=safe_user_name,
        post_content=safe_content,
        post_tags=rendered_tags
    )
    return html_output.strip()