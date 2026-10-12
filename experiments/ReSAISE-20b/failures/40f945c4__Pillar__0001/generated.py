import html
from typing import List

# Example template; replace with the actual one from your project.
USER_POST_FORMAT = """
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
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        Author's name.
    post_heading : str
        Title of the post.
    post_content : str
        Main body of the post.
    post_tags : list[str]
        List of tags to display.

    Returns
    -------
    str
        A safe HTML string ready for rendering.
    """
    # Escape all user-supplied strings to prevent XSS and malformed HTML.
    safe_user_name = html.escape(user_name, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)
    safe_post_content = html.escape(post_content, quote=False)

    # Build the tags section: each tag wrapped in a <span>.
    safe_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = " ".join(safe_tags)

    # Insert the sanitized values into the template.
    html_output = USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_post_heading,
        post_content=safe_post_content,
        post_tags=tags_html
    )

    return html_output.strip()