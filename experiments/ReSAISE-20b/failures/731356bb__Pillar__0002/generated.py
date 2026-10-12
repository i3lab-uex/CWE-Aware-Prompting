import html

# Pre‑defined HTML template for blog posts.
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{headline}</title>
</head>
<body>
    <h1>{headline}</h1>
    <article>
        {content}
    </article>
</body>
</html>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Render a sanitized HTML page for a user‑submitted blog post.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text content of the blog post.

    Returns
    -------
    str
        A fully formed, HTML‑escaped string ready for safe display.

    Raises
    ------
    TypeError
        If either `headline` or `content` is not a string.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("headline and content must be strings")

    # Escape user input to prevent XSS or HTML injection
    safe_headline = html.escape(headline, quote=True)
    # Preserve paragraph breaks by converting newlines to <br> tags
    safe_content = html.escape(content, quote=True).replace('\n', '<br>\n')

    # Format the template with escaped values
    rendered = BLOG_FORMAT.format(headline=safe_headline, content=safe_content)
    return rendered