import html
from typing import List

# Predefined template.  The placeholders are named exactly as the argument names
USER_POST_FORMAT: str = """
<div class="forum-post">
    <h2>{title_key}</h2>
    <p><strong>Posted by:</strong> {username_key}</p>
    <div class="post-body">{body_key}</div>
    <div class="tags">
        {tag_elements}
    </div>
</div>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str],
) -> str:
    """
    Return a safe HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        Identifier or display name of the user who created the post.
    title_key : str
        Title of the post.
    body_key : str
        Main content/body of the post.
    tag_elements : List[str]
        A list of tags to associate with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for rendering in a browser.

    Notes
    -----
    All user‑supplied strings are escaped using :func:`html.escape`
    to prevent injection of arbitrary markup or scripts.
    """
    # Escape all user‑provided strings
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=False)  # allow basic formatting like <br>

    # Wrap each tag in a <span> element, escaping the tag text
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    ]
    safe_tags = " ".join(escaped_tags)

    # Format the template with the escaped values
    rendered_html = USER_POST_FORMAT.format(
        username_key=safe_username,
        title_key=safe_title,
        body_key=safe_body,
        tag_elements=safe_tags,
    )

    return rendered_html.strip()