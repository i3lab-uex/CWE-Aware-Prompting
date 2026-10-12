import html

# Predefined template for a blog post.  
# The placeholders `{title}` and `{body}` will be safely substituted.
BLOG_FORMAT: str = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">\n{body}\n  </div>\n"
    "</article>"
)

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a user‑submitted blog post for safe display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post,
        ready for insertion into a webpage.

    Raises
    ------
    TypeError
        If either ``subject`` or ``description`` is not a string.
    """
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Escape any HTML special characters to prevent injection attacks
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Indent the body for readability in the final output
    indented_body = "\n".join("    " + line for line in safe_body.splitlines())

    # Format the blog post using the predefined template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=indented_body)

    return formatted_post