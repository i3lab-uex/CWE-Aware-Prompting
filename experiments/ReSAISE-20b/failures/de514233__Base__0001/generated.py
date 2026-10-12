import html

# Predefined template for blog posts.
# Example: "<h1>{title}</h1><p>{body}</p>"
BLOG_FORMAT = "<article>\n  <header><h1>{title}</h1></header>\n  <section>{body}</section>\n</article>"

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        A string containing the escaped and formatted blog post.
    """
    # Escape all user-provided content to prevent XSS
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the post using the predefined template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post