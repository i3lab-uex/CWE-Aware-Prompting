import html

# A simple HTML template for a blog entry.
# It uses `{title}` and `{body}` as placeholders that will be replaced
# by the sanitized values of `heading` and `content`.
BLOG_FORMAT = """
<article class="blog-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a safe, formatted HTML representation of a blog entry.

    Parameters
    ----------
    heading : str
        The title/heading of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post ready for display.

    Raises
    ------
    ValueError
        If either `heading` or `content` is not a string.
    """
    # Basic type validation
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")

    # Escape HTML special characters to prevent XSS attacks.
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Format the blog post using the predefined template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post