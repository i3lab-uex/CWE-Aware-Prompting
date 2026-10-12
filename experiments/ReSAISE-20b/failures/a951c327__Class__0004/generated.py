import html
from typing import List

# Predefined HTML template. Use placeholders that will be replaced by sanitized values.
USER_POST_FORMAT = """
<article class="post">
  <header>
    <h2>{title}</h2>
    <p class="author">Posted by {author}</p>
  </header>
  <section class="content">
    {body}
  </section>
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
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A string containing safe HTML that can be embedded in a web page.

    Notes
    -----
    All user-supplied data is escaped using html.escape to mitigate
    CWE-74 (HTML injection). The tags are rendered as individual <span>
    elements with a CSS class for styling.
    """
    # Escape user input to prevent HTML injection
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    # For body we escape but preserve line breaks as <br> for readability
    safe_body = html.escape(body, quote=True).replace('\n', '<br>')

    # Render tags as <span class="tag">escaped_tag</span>
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=safe_tags
    )