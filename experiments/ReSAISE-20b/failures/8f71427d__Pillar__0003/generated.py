import html
from typing import List

# Predefined HTML template with placeholders.  Use {username}, {title},
# {body} and {tags} to inject content safely.
USER_POST_FORMAT = """
<div class="user-post">
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
    Generate a secure HTML representation of a user's forum post.

    Args:
        username_key: The identifier of the post's creator.
        title_key: The heading of the user's post.
        body_key: The primary content of the user's post.
        tag_elements: A sequence of tags associated with the post.

    Returns:
        A string containing an XSS‑protected HTML version of the user's forum post.
    """
    # Escape all user supplied data to prevent XSS.
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=False)

    # Build the tags string: each tag is wrapped in a <span> element.
    safe_tags = []
    for tag in tag_elements:
        # Ensure the tag itself is escaped; do not allow injection of markup.
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = ' '.join(safe_tags)

    # Insert the escaped components into the template.
    rendered_html = USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )

    return rendered_html.strip()