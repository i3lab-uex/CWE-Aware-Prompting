import html
from typing import List

# Example template with placeholders; in a real application this would be defined elsewhere
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author_name}</p>
    <div class="content">{content}</div>
    <div class="tags">{tags}</div>
</div>
"""

def create_post_html(
    author_name: str,
    post_title: str,
    content: str,
    post_tags: List[str]
) -> str:
    """
    Build a safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the post's author.
    post_title : str
        Title/headline of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        List of tags to be displayed.

    Returns
    -------
    str
        XSS‑protected HTML string for the post.
    """
    # Escape user‑supplied data to prevent XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)

    # Render tags: each tag inside a <span>, escaped individually
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Fill the template with safe values
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )