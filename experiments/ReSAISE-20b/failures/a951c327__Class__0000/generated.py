import html
from typing import List

# Predefined HTML template with placeholders for author, title, body and tags.
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

def generate_post_html(author: str, title: str, body: str, post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The name of the user who authored the post.
    title : str
        The title of the post.
    body : str
        The main content of the post.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A string containing safe HTML for rendering the post.
    """
    # Escape all user-supplied content to prevent XSS and injection attacks
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)  # Preserve line breaks

    # Convert tags into a series of <span> elements, escaping each tag
    safe_tags = "".join(f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in post_tags)

    # Render the final HTML
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body.replace("\n", "<br>"),
        tags=safe_tags
    )