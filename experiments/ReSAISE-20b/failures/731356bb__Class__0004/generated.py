import html

# Example HTML template with placeholders for title and body.
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
    Formats and sanitizes a blog post for safe display on a webpage.

    Args:
        headline (str): The title of the blog post.
        content (str): The full text content of the blog post.

    Returns:
        str: A fully-formed HTML string with the title and content safely escaped.
    """
    # Escape user-provided input to prevent HTML injection (CWE-74)
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)