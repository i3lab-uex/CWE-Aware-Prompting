import html

# Predefined HTML structure for a blog post.
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
    <div class="content">
        {text}
    </div>
</article>
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
        A fully sanitized and HTML‑formatted blog post ready for rendering.

    Raises
    ------
    ValueError
        If either ``heading`` or ``text`` is empty.
    """
    if not heading:
        raise ValueError("Heading cannot be empty.")
    if not text:
        raise ValueError("Text content cannot be empty.")

    # Escape user input to prevent XSS and ensure well‑formedness.
    safe_heading = html.escape(heading, quote=True)
    # Preserve line breaks in the body by converting newlines to <br>.
    safe_text = html.escape(text, quote=True).replace("\n", "<br>\n")

    # Insert sanitized content into the template.
    return BLOG_FORMAT.format(heading=safe_heading, text=safe_text)