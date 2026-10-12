import html
from typing import List

# Example template with placeholders for the post components.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">by {author}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(author: str, title: str, body: str,
                       post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The author's name.
    title : str
        The post's title.
    body : str
        The main content of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The HTML string for the post, safely escaped to prevent XSS.
    """
    # Escape all user-supplied content
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body)

    # Convert tags to a series of <span> elements
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Format the template with sanitized values
    return USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )