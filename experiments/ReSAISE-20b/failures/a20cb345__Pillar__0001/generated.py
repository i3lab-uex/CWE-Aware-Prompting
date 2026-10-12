import html

# Example template – in real use this should be defined elsewhere and imported.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{subject}</h1>\n"
    "  <div class=\"content\">{description}</div>\n"
    "</article>"
)

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a blog post for safe display.

    Parameters
    ----------
    subject : str
        The title of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A fully sanitized, HTML‑escaped string ready to be injected into a page.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    # Validate input types
    if not isinstance(subject, str):
        raise TypeError(f"subject must be a string, got {type(subject).__name__}")
    if not isinstance(description, str):
        raise TypeError(f"description must be a string, got {type(description).__name__}")

    # Escape potentially dangerous characters to prevent XSS
    safe_subject = html.escape(subject, quote=True)
    safe_description = html.escape(description, quote=True)

    # Use keyword formatting to avoid accidental placeholder injection
    formatted = BLOG_FORMAT.format(subject=safe_subject, description=safe_description)

    return formatted