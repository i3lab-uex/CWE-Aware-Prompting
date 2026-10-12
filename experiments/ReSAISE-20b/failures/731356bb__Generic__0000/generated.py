import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with the
# sanitized headline and content respectively.
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 2rem;}}
        h1 {{color: #333;}}
    </style>
</head>
<body>
    <article>
        <h1>{title}</h1>
        <div>{body}</div>
    </article>
</body>
</html>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Render a user‑submitted blog post safely for display on the web.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text body of the blog post.

    Returns
    -------
    str
        A sanitized HTML string ready to be served to a client.
    """
    # Sanitize user input to prevent XSS attacks
    safe_title = html.escape(headline, quote=True)
    # Preserve line breaks by converting newlines to <br> tags
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")
    
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)