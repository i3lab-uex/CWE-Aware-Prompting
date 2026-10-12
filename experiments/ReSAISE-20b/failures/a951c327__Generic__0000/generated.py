import html
from typing import List

# Example template. Replace placeholders with the actual keys.
USER_POST_FORMAT: str = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author}</p>
    <div class="body">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        Author of the post.
    title : str
        Title of the post.
    body : str
        Main content of the post.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string for rendering in a public forum.
    """
    # Escape user-provided content to prevent XSS
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False).replace('\n', '<br>')

    # Build the tags string: each tag inside a <span class="tag">
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )