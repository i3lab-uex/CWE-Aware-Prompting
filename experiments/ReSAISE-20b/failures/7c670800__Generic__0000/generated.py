import html

# Predefined template for formatting blog posts.
# Placeholders are `{title}` and `{body}` which will be replaced with sanitized values.
BLOG_FORMAT = "<article><h1>{title}</h1>\n<p>{body}</p></article>"

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a sanitized and formatted blog entry ready for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML of the blog post.

    Raises
    ------
    TypeError
        If either `heading` or `content` is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError(f"Expected `heading` to be a string, got {type(heading).__name__}")
    if not isinstance(content, str):
        raise TypeError(f"Expected `content` to be a string, got {type(content).__name__}")

    # Escape any HTML characters to prevent XSS attacks.
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Format the sanitized values into the template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post