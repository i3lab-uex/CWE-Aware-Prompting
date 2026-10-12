import html

# Predefined HTML template for blog posts.
# It must contain the placeholders {title} and {body}.
BLOG_FORMAT: str = """
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
    Render a user‑submitted blog post safely for display on a webpage.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    content : str
        The full text content of the blog post.

    Returns
    -------
    str
        A complete HTML page with the title and body inserted, with all user
        input properly escaped to prevent XSS or malformed HTML.

    Raises
    ------
    ValueError
        If either headline or content is empty.
    """
    if not headline:
        raise ValueError("Headline cannot be empty.")
    if not content:
        raise ValueError("Content cannot be empty.")

    # Escape user input to neutralize any HTML/JS that might have been injected.
    safe_title = html.escape(headline, quote=True)
    # Convert newlines to <br> for simple formatting; escape first.
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)