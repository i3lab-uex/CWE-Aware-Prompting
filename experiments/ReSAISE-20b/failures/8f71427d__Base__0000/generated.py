import html
from typing import List

# Example template (can be replaced with the real one)
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p><strong>Author:</strong> {author}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str]
) -> str:
    """
    Generate a secure HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        The identifier of the post's creator.
    title_key : str
        The heading/title of the user's post.
    body_key : str
        The primary content/body of the user's post.
    tag_elements : List[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for the forum post.
    """
    # Escape all user-supplied input
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=True)

    # Wrap each tag in a <span> and escape its content
    safe_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    ]
    tags_html = ' '.join(safe_tags)

    # Populate the template with escaped values
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_username,
        body=safe_body,
        tags=tags_html
    )