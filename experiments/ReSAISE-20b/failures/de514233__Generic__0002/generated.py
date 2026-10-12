import html

# Predefined template for blog posts.
# It should contain placeholders `{title}` and `{body}` that will be
# replaced with the sanitized title and content.
BLOG_FORMAT: str = (
    "<article>\n"
    "  <header><h1>{title}</h1></header>\n"
    "  <section>{body}</section>\n"
    "</article>"
)

def show_blog_post(headline: str, text: str) -> str:
    """
    Sanitize and format a user‑submitted blog post.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main content/body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML ready for display.

    Raises
    ------
    TypeError
        If either `headline` or `text` is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Escape HTML special characters to prevent XSS attacks.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the post using the predefined template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_post