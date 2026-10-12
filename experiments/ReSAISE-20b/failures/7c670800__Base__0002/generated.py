import html

# Example template; adjust as needed for the actual application.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">{body}</div>\n"
    "</article>"
)

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a sanitized and formatted blog entry ready for safe HTML display.

    Parameters
    ----------
    heading : str
        The title of the blog post. User‑controlled input.
    content : str
        The body text of the blog post. User‑controlled input.

    Returns
    -------
    str
        An HTML string with the title and content safely escaped.
    """
    # Escape user input to prevent XSS (CWE‑79)
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Insert escaped values into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)