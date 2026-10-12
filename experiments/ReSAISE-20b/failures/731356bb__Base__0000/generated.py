import html

# Predefined HTML template for a blog post.
# The placeholders `{title}` and `{body}` will be replaced with sanitized content.
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
<article>
    <h1>{title}</h1>
    <div class="content">
        {body}
    </div>
</article>
</body>
</html>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Format a blog post for safe HTML display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text body of the blog post.

    Returns
    -------
    str
        A fully rendered, sanitized HTML string ready to be served.

    Notes
    -----
    - Uses html.escape to neutralize any potentially malicious content.
    - The function does not perform any further sanitization beyond escaping
      characters that have special meaning in HTML.
    """
    # Escape user-supplied input to prevent XSS (CWE-79)
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Insert the sanitized values into the template
    rendered_html = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return rendered_html