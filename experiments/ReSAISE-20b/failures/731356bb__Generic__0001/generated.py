import html

# Example template; replace with the actual one used in your project.
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
    Render a blog post into an HTML page safely.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full body text of the blog post.

    Returns
    -------
    str
        A complete HTML string with the title and body inserted,
        safely escaped to prevent XSS attacks.

    Raises
    ------
    ValueError
        If either headline or content is empty.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("headline and content must be strings")

    if headline.strip() == "" or content.strip() == "":
        raise ValueError("headline and content must not be empty")

    # Escape user-provided text to avoid injection
    safe_title = html.escape(headline, quote=True)
    # Preserve line breaks in content by converting newlines to <br>
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)