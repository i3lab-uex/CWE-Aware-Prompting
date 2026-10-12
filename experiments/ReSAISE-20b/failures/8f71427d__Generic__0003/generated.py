import html
from typing import List

# Predefined template containing placeholders for the post's components.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title_key}</h2>
  <p class="author">Posted by: {username_key}</p>
  <div class="content">{body_key}</div>
  <div class="tags">{tag_elements}</div>
</div>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str]
) -> str:
    """
    Generate a secure HTML representation of a user's forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        Heading of the user's post.
    body_key : str
        Primary content of the user's post.
    tag_elements : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS-protected HTML string for rendering the post.
    """
    # Escape all user-supplied content to avoid XSS
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=False)  # Preserve newlines etc.

    # Wrap each tag in a <span> and escape the tag text
    safe_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    ]
    tags_html = ' '.join(safe_tags)

    # Render the final HTML using the template
    rendered_html = USER_POST_FORMAT.format(
        username_key=safe_username,
        title_key=safe_title,
        body_key=safe_body,
        tag_elements=tags_html
    )

    return rendered_html.strip()