import html
from typing import List

# Example template (the real one is assumed to be defined elsewhere)
USER_POST_FORMAT = """
<div class="post">
  <h1>{title}</h1>
  <p class="author">Posted by {author_name}</p>
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
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        The name of the user who authored the post.
    post_title : str
        The title (headline) of the post.
    content : str
        The main body text of the post.
    post_tags : List[str]
        A list of tags that apply to this post.

    Returns
    -------
    str
        An HTML string safely escaped for inclusion in a web page.
    """
    # Escape all user‑supplied text to avoid XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)

    # Build the tags string
    tag_spans = []
    for tag in post_tags:
        safe_tag = html.escape(tag, quote=True)
        tag_spans.append(f'<span class="tag">{safe_tag}</span>')
    tags_html = " ".join(tag_spans)

    # Format the final HTML using the provided template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=tags_html
    )