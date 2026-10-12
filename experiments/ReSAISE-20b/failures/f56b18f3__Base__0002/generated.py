import html

# Predefined HTML template for a blog post.
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
        <div class="content">{body}</div>
    </article>
</body>
</html>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Sanitize and format a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for safe presentation on a webpage.

    Raises
    ------
    ValueError
        If either `heading` or `text` is not a string.
    """
    if not isinstance(heading, str) or not isinstance(text, str):
        raise ValueError("Both heading and text must be strings.")

    # Escape all special HTML characters to prevent XSS.
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(text, quote=True)

    # Replace newlines with <br> for display formatting.
    safe_body = safe_body.replace("\n", "<br>")

    # Return the final HTML.
    return BLOG_FORMAT.format(heading=safe_heading, body=safe_body)