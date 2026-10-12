import html

# Predefined HTML structure for a blog post.
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

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user-submitted blog post for secure web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready for rendering on the webpage.

    Raises
    ------
    ValueError
        If either heading or text is empty.
    """
    if not heading:
        raise ValueError("Heading cannot be empty.")
    if not text:
        raise ValueError("Text content cannot be empty.")

    # Escape all HTML special characters to prevent injection.
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(text, quote=True)

    # Replace newlines with <br> tags for proper formatting in the browser.
    safe_body = safe_body.replace('\n', '<br>')

    return BLOG_FORMAT.format(title=safe_heading, body=safe_body)