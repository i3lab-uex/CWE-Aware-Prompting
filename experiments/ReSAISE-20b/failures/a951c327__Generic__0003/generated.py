import html
from typing import List

# Example template – adjust placeholders as needed for the actual application.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a user's forum post.

    Parameters
    ----------
    author : str
        The name of the user who authored the post.
    title : str
        The post's title.
    body : str
        The main content of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string that can safely be embedded in a web page.
    """
    # Escape all user-provided content to prevent XSS attacks
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)  # preserve line breaks and formatting

    # Build the tags string: each tag wrapped in a <span> element
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Populate the template with sanitized values
    return USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body.replace('\n', '<br>'),  # preserve newlines
        tags=safe_tags
    )