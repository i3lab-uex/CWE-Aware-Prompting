import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced by the user supplied values.
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
    Formats a user‑submitted blog post into safe HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full text body of the blog post.

    Returns
    -------
    str
        A fully rendered HTML string with user input properly escaped to
        prevent XSS attacks (CWE‑79).

    Raises
    ------
    TypeError
        If either `headline` or `content` is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # Escape user input to neutralize any malicious scripts.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Construct the final HTML page.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)