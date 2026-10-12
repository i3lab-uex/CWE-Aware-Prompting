import html
from typing import List

# Predefined template for a user post.  The placeholders will be replaced
# by the escaped values of username, title, body and tags.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {username}</p>
    <div class="content">{body}</div>
    <div class="tags">
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
    Generate an XSS‑protected HTML representation of a user’s forum post.

    Parameters
    ----------
    username_key : str
        Identifier (username) of the post’s creator.
    title_key : str
        Title/heading of the user’s post.
    body_key : str
        Primary content of the post.
    tag_elements : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing safe, escaped HTML for the user post.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or not strings.
    """
    # Basic type checking
    if not all(isinstance(arg, str) for arg in (username_key, title_key, body_key)):
        raise ValueError("Username, title and body must be strings.")
    if not isinstance(tag_elements, list):
        raise ValueError("tag_elements must be a list of strings.")
    if not all(isinstance(tag, str) for tag in tag_elements):
        raise ValueError("All tags must be strings.")

    # Escape user supplied data to neutralize special characters
    safe_username = html.escape(username_key, quote=True)
    safe_title   = html.escape(title_key,     quote=True)
    safe_body    = html.escape(body_key,      quote=True)

    # Wrap each tag in a <span> element and escape the tag text
    escaped_tags = []
    for tag in tag_elements:
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')
    safe_tag_elements = " ".join(escaped_tags)

    # Construct the final HTML using the template
    rendered_html = USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tag_elements=safe_tag_elements
    )
    return rendered_html.strip()