import html

# Predefined HTML template for blog posts.
# The placeholders {title} and {body} will be replaced by the sanitized values.
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
    Formats a blog post for safe display on a webpage.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post.

    Raises
    ------
    ValueError
        If either headline or content is not a string.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise ValueError("Both headline and content must be strings")

    # Sanitize inputs to avoid XSS or HTML injection.
    safe_headline = html.escape(headline, quote=True)
    # Preserve line breaks by converting them to <br> tags after escaping.
    safe_content = html.escape(content, quote=True).replace('\n', '<br>\n')

    # Populate the template.
    rendered = BLOG_FORMAT.format(title=safe_headline, body=safe_content)

    return rendered