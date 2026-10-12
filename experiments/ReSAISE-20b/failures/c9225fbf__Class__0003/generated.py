import html
from typing import List

# Example template with placeholders.
# In real usage this should be imported or defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p><strong>Author:</strong> {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">{tags}</div>
</div>
"""

def create_post_html(author_name: str,
                     post_title: str,
                     content: str,
                     post_tags: List[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        The name of the post's author.
    post_title : str
        The headline of the user's post.
    content : str
        The primary text content of the user's post.
    post_tags : List[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        An HTML string with all user input safely escaped and tags wrapped in <span> elements.
    """
    # Escape all user-supplied text to prevent injection attacks
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build tags: each tag is escaped and wrapped in a <span>
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Populate the template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )