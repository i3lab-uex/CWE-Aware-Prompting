import html
from typing import Final

# Pre‑defined HTML template for a blog post.  
# The placeholders {title} and {body} will be replaced with the
# escaped headline and content.
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Return a fully escaped and HTML‑formatted blog post.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text of the blog post.

    Returns
    -------
    str
        A string containing the rendered HTML. The headline and content
        are escaped to prevent XSS, newlines in the content are converted
        to <br> tags for proper rendering.

    Raises
    ------
    ValueError
        If either argument is not a string.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise ValueError("Both headline and content must be strings")

    # Escape special HTML characters to prevent injection.
    safe_title = html.escape(headline, quote=True)
    # Escape content and preserve line breaks.
    escaped_content = html.escape(content, quote=True).replace("\n", "<br>")

    # Use format to insert the sanitized values into the template.
    rendered = BLOG_FORMAT.format(title=safe_title, body=escaped_content)
    return rendered