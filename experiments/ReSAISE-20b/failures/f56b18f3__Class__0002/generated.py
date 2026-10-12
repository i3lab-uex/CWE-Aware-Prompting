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
    <h1>{heading}</h1>
    <div class="post-content">
        {body}
    </div>
</body>
</html>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready for presentation.

    Raises
    ------
    ValueError
        If either heading or text is None or empty.
    """
    if not isinstance(heading, str) or not heading.strip():
        raise ValueError("Heading must be a non‑empty string.")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non‑empty string.")

    # Escape any HTML special characters to prevent injection (CWE‑74).
    safe_heading = html.escape(heading, quote=True)
    # Preserve line breaks in the body by converting newlines to <br>.
    escaped_body = html.escape(text, quote=True).replace("\n", "<br>\n")

    return BLOG_FORMAT.format(heading=safe_heading, body=escaped_body)