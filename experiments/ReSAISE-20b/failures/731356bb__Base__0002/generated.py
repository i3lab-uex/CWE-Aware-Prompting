import html

# Pre‑defined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Render a blog post page by sanitizing user input and inserting it into
    the BLOG_FORMAT template.

    Parameters:
        headline (str): The title of the blog post.
        content (str): The full text content of the blog post.

    Returns:
        str: A safe, HTML‑formatted string ready for inclusion in a web page.

    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("headline and content must be strings")

    # Escape HTML special characters to prevent XSS (CWE‑79)
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Insert sanitized values into the template
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)