import html

# Predefined HTML structure with placeholders for title and body.
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{heading}</title>
</head>
<body>
<article>
    <h1>{heading}</h1>
    <div class="post-body">
        {body}
    </div>
</article>
</body>
</html>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Sanitize and format a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A fully formed HTML string ready to be served in a web page.

    Raises
    ------
    ValueError
        If either heading or text is empty.
    """
    if not heading:
        raise ValueError("Heading must not be empty.")
    if not text:
        raise ValueError("Text must not be empty.")

    # Escape user-provided content to prevent XSS (CWE-79).
    safe_heading = html.escape(heading, quote=True)
    # Convert line breaks to <br> for preserving formatting.
    safe_body = html.escape(text, quote=True).replace('\n', '<br>\n')

    return BLOG_FORMAT.format(heading=safe_heading, body=safe_body)