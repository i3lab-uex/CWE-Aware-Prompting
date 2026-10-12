import html
from typing import List

# Predefined HTML template with placeholders:
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author_name}</p>
  <div class="content">{body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def render_forum_post(author_name: str,
                      title: str,
                      body_content: str,
                      tag_list: List[str]) -> str:
    """
    Generate a secure, XSS‑protected HTML representation of a forum post.

    Args:
        author_name (str): Identifier of the post's creator.
        title (str): Heading of the user's post.
        body_content (str): Primary content of the user's post.
        tag_list (List[str]): Sequence of tags associated with the post.

    Returns:
        str: The fully escaped HTML string for rendering.
    """
    # Escape all user‑supplied strings to neutralize special characters
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # body may contain newlines

    # Build tags: each tag is escaped and wrapped in <span>
    safe_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    ]
    tags_html = ' '.join(safe_tags)

    # Render the final HTML using the template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )