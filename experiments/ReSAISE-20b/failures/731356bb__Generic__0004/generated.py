import html

# Pre‑defined HTML template for a blog post. The placeholders `{title}` and `{body}`
# will be replaced by the sanitized user input.
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
    <div class="content">{body}</div>
</article>
</body>
</html>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Render a user‑submitted blog post into safe HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text body of the blog post.

    Returns
    -------
    str
        A complete HTML page with the title and content safely escaped.
    """
    # Escape user input to prevent XSS attacks
    safe_title = html.escape(headline, quote=True)
    # Preserve line breaks in content by converting newlines to <br>
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    # Populate the template
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return rendered