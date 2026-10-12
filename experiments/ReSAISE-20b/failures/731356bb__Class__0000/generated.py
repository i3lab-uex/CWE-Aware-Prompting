import html

# Predefined HTML template for a blog post.
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
    Formats and sanitizes a blog post for safe HTML display.

    Args:
        headline (str): The title of the blog post.
        content (str): The full text content of the blog post.

    Returns:
        str: A complete HTML page string with the title and body inserted safely.
    """
    # Escape any special characters to prevent XSS or HTML injection
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Inject the escaped values into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)