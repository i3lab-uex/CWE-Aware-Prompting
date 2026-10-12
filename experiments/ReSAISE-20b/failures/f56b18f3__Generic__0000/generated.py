import html

# Example HTML template with placeholders for the title and body.
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{heading}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #333; }}
        p {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>{heading}</h1>
    <div class="content">{body}</div>
</body>
</html>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A fully formatted, HTML‑escaped blog post ready for rendering.

    Raises
    ------
    ValueError
        If either heading or text is empty after stripping whitespace.
    """
    # Basic validation: non-empty strings
    if not heading or not heading.strip():
        raise ValueError("Heading cannot be empty.")
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    # Escape user input to prevent XSS attacks
    safe_heading = html.escape(heading.strip(), quote=True)
    # Convert newlines to <br> for paragraph breaks
    safe_body = html.escape(text.strip(), quote=True).replace("\n", "<br>")

    # Populate the template
    formatted_post = BLOG_FORMAT.format(heading=safe_heading, body=safe_body)

    return formatted_post