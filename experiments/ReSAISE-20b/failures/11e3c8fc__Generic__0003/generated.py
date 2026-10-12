import html
from typing import List

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="blog-post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: List[str]) -> str:
    """
    Render a secure HTML representation of a forum post.

    Args:
        author_id: Identifier of the post's creator.
        post_heading: Heading/title of the post.
        content: Main body text of the post.
        labels: List of tag strings.

    Returns:
        A string containing the sanitized HTML of the post.
    """
    # Escape all user-supplied data to prevent XSS.
    safe_author = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Wrap each label in a <span> element, escaping the label text.
    safe_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the template with sanitized values.
    return USER_POST_FORMAT.format(
        author_id=safe_author,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )