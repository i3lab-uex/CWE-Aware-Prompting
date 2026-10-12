import html

# Predefined template for blog posts.
# Example: "<h1>{title}</h1><div class=\"content\">{body}</div>"
BLOG_FORMAT = "<article><header><h1>{title}</h1></header><section class=\"post-body\">{body}</section></article>"

def display_blog_entry(heading: str, content: str) -> str:
    """
    Sanitize and format a blog entry for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML ready for display.

    Raises
    ------
    TypeError
        If either `heading` or `content` is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError(f"Expected heading to be a string, got {type(heading).__name__}")
    if not isinstance(content, str):
        raise TypeError(f"Expected content to be a string, got {type(content).__name__}")

    # Escape HTML special characters to prevent XSS
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Format using the predefined template
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_entry