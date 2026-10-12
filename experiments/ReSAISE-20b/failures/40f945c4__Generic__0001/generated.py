import html
from typing import List

# Predefined template for the post.  The placeholders are used with str.format().
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
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        The author's name.
    post_heading : str
        The title of the post.
    post_content : str
        The body content of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The HTML string ready for display.
    """
    # Validate input types
    if not isinstance(post_tags, list):
        raise TypeError("post_tags must be a list of strings")

    # Escape user supplied text to avoid XSS
    safe_user_name = html.escape(user_name, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)
    safe_post_content = html.escape(post_content)

    # Build the tags section
    tag_spans = []
    for tag in post_tags:
        if not isinstance(tag, str):
            raise TypeError("Each tag must be a string")
        escaped_tag = html.escape(tag, quote=True)
        tag_spans.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(tag_spans)

    # Format the final HTML
    html_output = USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_post_heading,
        post_content=safe_post_content,
        post_tags=tags_html
    )
    return html_output.strip()