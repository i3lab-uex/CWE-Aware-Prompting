import html
from typing import List

# A minimal HTML template for a forum post.
# {author}, {title}, {body} and {tags_html} will be substituted safely.
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
    {tags_html}
  </footer>
</article>
"""

def _escape(text: str) -> str:
    """
    Safely escape text for inclusion in HTML.
    """
    return html.escape(text, quote=True)

def _render_tags(tags: List[str]) -> str:
    """
    Render a list of tags as <span> elements, each escaped.
    """
    if not tags:
        return ''
    rendered = []
    for tag in tags:
        escaped_tag = _escape(tag)
        rendered.append(f'<span class="tag">{escaped_tag}</span>')
    return ' '.join(rendered)

def generate_post_html(author: str, title: str, body: str,
                       post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The username or display name of the poster.
    title : str
        The post's title.
    body : str
        The main content of the post. HTML tags are preserved but
        attributes are not parsed; only plain text is escaped.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The complete HTML snippet for the post, with all user‑supplied data escaped.
    """
    # Escape all dynamic content to prevent XSS and HTML injection
    safe_author = _escape(author)
    safe_title = _escape(title)
    # Body is treated as plain text; escape it to avoid rendering user HTML
    safe_body = _escape(body)

    tags_html = _render_tags(post_tags)

    # Use format_map to avoid accidental replacement of braces in content
    html_snippet = USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body,
        tags_html=tags_html
    )
    return html_snippet.strip()