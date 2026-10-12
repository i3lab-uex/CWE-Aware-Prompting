import html
from typing import List

# Predefined template with placeholders for the post components.
USER_POST_FORMAT = """
<article class="post">
  <h2>{title}</h2>
  <p class="author">Posted by {author}</p>
  <div class="content">{body}</div>
  <footer class="tags">
    {tags}
  </footer>
</article>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a user's forum post.

    Parameters
    ----------
    author : str
        The author's name.
    title : str
        The post's title.
    body : str
        The main content of the post.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string for embedding in a page.
    """
    # Escape user-supplied content to prevent XSS and ensure well‑formedness.
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain HTML entities but we escape all.

    # Render tags as individual <span> elements, each escaped.
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Insert the sanitized parts into the template.
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=safe_tags
    )