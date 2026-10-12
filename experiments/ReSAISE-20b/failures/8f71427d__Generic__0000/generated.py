import html
from typing import List

# A simple template for the forum post. Placeholders are named for clarity.
USER_POST_FORMAT = """
<div class="forum-post">
    <h2>{title_key}</h2>
    <p><strong>Author:</strong> {username_key}</p>
    <div class="post-body">{body_key}</div>
    <div class="post-tags">
        {tag_elements}
    </div>
</div>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str]
) -> str:
    """
    Generate a safe HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        The heading/title of the user's post.
    body_key : str
        The main content/body of the post.
    tag_elements : List[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS-protected HTML string for the forum post.
    """
    # Escape all user-supplied text to prevent XSS
    escaped_username = html.escape(username_key, quote=True)
    escaped_title = html.escape(title_key, quote=True)
    escaped_body = html.escape(body_key)

    # Wrap each tag in a <span> and escape the tag text
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    ]
    tags_html = " ".join(escaped_tags)

    # Render the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        username_key=escaped_username,
        title_key=escaped_title,
        body_key=escaped_body,
        tag_elements=tags_html
    )