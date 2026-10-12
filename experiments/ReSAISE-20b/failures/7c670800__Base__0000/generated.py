import html

# Predefined template for a blog post. The placeholders `{title}` and `{body}`
# will be replaced with the sanitized title and content respectively.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">\n{body}\n  </div>\n"
    "</article>"
)

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a sanitized and formatted HTML string for a blog post.

    Args:
        heading: The title of the blog post.
        content: The main text content of the blog post.

    Returns:
        A string containing safe HTML ready for rendering on a webpage.
    """
    # Escape all user-supplied input to prevent XSS (CWE-79).
    safe_title = html.escape(heading, quote=True)
    # Escape newlines as <br> to preserve formatting in the body.
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)