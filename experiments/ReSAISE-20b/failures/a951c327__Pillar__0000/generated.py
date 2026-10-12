import html
from typing import List

# A simple HTML template for a forum post. The placeholders will be replaced with
# sanitized values.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author}</p>
  <div class="content">{body}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def _sanitize_tag(tag: str) -> str:
    """
    Sanitize a single tag by allowing only alphanumeric characters and hyphens.
    Any other character is stripped to prevent injection of malicious code.
    """
    # Keep only safe characters
    allowed = "".join(ch for ch in tag if ch.isalnum() or ch == "-")
    # Escape any remaining special characters (should be none, but for safety)
    return html.escape(allowed)

def generate_post_html(author: str,
                       title: str,
                       body: str,
                       post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a user's forum post.

    Args:
        author: The name of the author.
        title: Title of the post.
        body: Main content of the post.
        post_tags: List of tags associated with the post.

    Returns:
        A string containing sanitized HTML that can be safely rendered in a browser.
    """
    # Escape all user-supplied content
    safe_author = html.escape(author)
    safe_title = html.escape(title)
    safe_body = html.escape(body)

    # Sanitize tags and wrap each in a <span>
    safe_tag_spans = []
    for tag in post_tags:
        sanitized = _sanitize_tag(tag)
        if sanitized:  # Skip empty tags
            safe_tag_spans.append(f'<span class="tag">{sanitized}</span>')

    tags_html = " ".join(safe_tag_spans)

    # Render the final HTML using the template
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=tags_html
    )