import html

# Predefined HTML template for a blog post.
# {title} and {body} will be replaced with the sanitized content.
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #333; }}
        .content {{ line-height: 1.6; white-space: pre-wrap; }}
    </style>
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
    Format and sanitize a blog post for safe HTML display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full body text of the blog post.

    Returns
    -------
    str
        A fully rendered HTML page with the title and content safely escaped.
    """
    # Escape any potentially dangerous characters to prevent XSS attacks.
    safe_title = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render the final HTML using the template.
    rendered_html = BLOG_FORMAT.format(title=safe_title, body=safe_content)
    return rendered_html