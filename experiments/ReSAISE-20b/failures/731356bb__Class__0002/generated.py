import html

# Predefined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with the escaped user input.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Render a blog post page from user-supplied title and content.

    Parameters
    ----------
    headline : str
        The headline or title of the blog post.
    content : str
        The full text content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML-formatted string ready for safe display on a webpage.

    Notes
    -----
    - The function escapes all HTML special characters in both headline and content to prevent
      injection attacks (CWE-74).
    - It uses a simple template with placeholders that are replaced after escaping.
    """
    # Escape user input to neutralize any HTML special characters
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Replace placeholders in the template with the escaped values
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return rendered