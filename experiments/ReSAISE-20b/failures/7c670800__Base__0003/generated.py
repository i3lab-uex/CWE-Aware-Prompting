import html

# Predefined template for a blog post.  The placeholders are `{title}` and `{body}`.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a safe, sanitized HTML representation of a blog entry.

    Parameters
    ----------
    heading : str
        The title of the blog post.  This will be escaped to prevent XSS.
    content : str
        The main body of the blog post.  This will be escaped to prevent XSS.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post ready for display.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(heading, str) or not isinstance(content, str):
        raise TypeError("Both heading and content must be strings.")

    # Escape user supplied data to neutralize malicious scripts.
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Format the sanitized content into the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)