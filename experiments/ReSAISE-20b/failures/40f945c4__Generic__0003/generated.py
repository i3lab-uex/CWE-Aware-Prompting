import html
from typing import List

# Example template; in real usage this should be defined elsewhere.
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
        Author of the post.
    post_heading : str
        Title of the post.
    post_content : str
        Main content of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing sanitized HTML for the post.
    """
    # Escape all user-supplied text to prevent XSS attacks
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(post_content)

    # Sanitize tags and wrap each in a <span>
    safe_tag_spans = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    safe_tags = " ".join(safe_tag_spans)

    # Render the template
    html_output = USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_heading,
        post_content=safe_content,
        post_tags=safe_tags
    )

    return html_output.strip()