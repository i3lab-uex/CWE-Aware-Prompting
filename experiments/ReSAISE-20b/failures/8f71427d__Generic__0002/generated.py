import html
from typing import List

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {username}</p>
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
    Generate a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        Heading/title of the user's post.
    body_key : str
        Primary content/body of the user's post.
    tag_elements : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for the forum post.
    """
    # Escape user‑supplied content to prevent XSS
    escaped_username = html.escape(username_key, quote=True)
    escaped_title = html.escape(title_key, quote=True)
    escaped_body = html.escape(body_key, quote=False)  # Preserve line breaks & whitespace

    # Wrap each tag in a <span> element and escape the tag text
    escaped_tags = []
    for tag in tag_elements:
        safe_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{safe_tag}</span>')

    tags_html = ' '.join(escaped_tags)

    # Render the final HTML using the template
    return USER_POST_FORMAT.format(
        username=escaped_username,
        title=escaped_title,
        body=escaped_body,
        tags=tags_html
    )