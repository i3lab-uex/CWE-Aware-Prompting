import html

# Example template; in real usage this should be defined elsewhere.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">\n{body}\n  </div>\n"
    "</article>"
)

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML of the blog post.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # Escape all HTML special characters to prevent XSS attacks.
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(content, quote=True)

    # The body may contain line breaks; preserve them as <br> tags.
    safe_body = safe_body.replace("\n", "<br>\n")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)