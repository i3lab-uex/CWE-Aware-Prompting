import html
from typing import List

# A simple template that will be used to render the post.
# The placeholders are named for readability and can be
# replaced with str.format or f-strings.
USER_POST_FORMAT: str = """
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
    Generate a safe HTML representation of a forum post.

    All user-provided input is escaped to prevent XSS attacks.
    Tags are rendered as individual <span> elements.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        The title of the user's post.
    post_content : str
        The main content of the user's post.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The sanitized HTML string for the post.
    """
    # Escape all user input to avoid injection
    escaped_user_name = html.escape(user_name, quote=True)
    escaped_heading = html.escape(post_heading, quote=True)
    escaped_content = html.escape(post_content, quote=False)

    # Build tags string: each tag wrapped in a <span> with escaped content
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = " ".join(escaped_tags)

    # Populate the template
    html_output = USER_POST_FORMAT.format(
        post_heading=escaped_heading,
        user_name=escaped_user_name,
        post_content=escaped_content,
        post_tags=tags_html
    )

    return html_output.strip()