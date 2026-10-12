import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="post">
  <h2>{title}</h2>
  <p class="meta">by {author}</p>
  <div class="content">{body}</div>
  <footer class="tags">
    {tags}
  </footer>
</article>
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
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing sanitized HTML ready to be served.

    Notes
    -----
    All user-supplied content is escaped using html.escape to prevent
    cross‑site scripting (CWE-79).  Tags are rendered as individual <span>
    elements with the class "tag".
    """
    # Escape user input to neutralize HTML special characters
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Render tags safely
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = " ".join(escaped_tags)

    # Populate the template
    return USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )