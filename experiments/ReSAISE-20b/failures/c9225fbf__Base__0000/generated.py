import html
from typing import List

# Example template (replace with the actual one used in your application)
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
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the user who posted.
    post_title : str
        Title/headline of the post.
    content : str
        Main body text of the post.
    post_tags : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string ready to be served.
    """
    # Escape all user‑supplied values
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)  # Preserve newlines

    # Build tags string: each tag wrapped in <span>, escaped
    safe_tags = ""
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags += f'<span class="tag">{escaped_tag}</span> '

    # Trim trailing space and insert into template
    formatted = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags.strip()
    )
    return formatted