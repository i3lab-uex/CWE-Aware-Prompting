import html
from typing import List

# Predefined HTML template.  It must contain placeholders for the four components:
#   {user_name}, {post_heading}, {post_content}, {post_tags}
USER_POST_FORMAT = """
<div class="user-post">
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
        The sanitized HTML string for rendering the post.

    Raises
    ------
    ValueError
        If any of the required parameters are None.
    """
    # Basic validation to avoid accidental None values
    if any(arg is None for arg in (user_name, post_heading, post_content, post_tags)):
        raise ValueError("All arguments must be non‑None")

    # Escape all user supplied content to prevent HTML injection (CWE-74)
    safe_user_name = html.escape(user_name, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)
    safe_post_content = html.escape(post_content, quote=True)

    # Convert tags to escaped <span> elements
    safe_tags = []
    for tag in post_tags:
        if tag is None:
            continue
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')

    # Join tags with a space for readability
    safe_post_tags = " ".join(safe_tags)

    # Format the final HTML using the predefined template
    rendered_html = USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_post_heading,
        post_content=safe_post_content,
        post_tags=safe_post_tags
    )

    return rendered_html.strip()