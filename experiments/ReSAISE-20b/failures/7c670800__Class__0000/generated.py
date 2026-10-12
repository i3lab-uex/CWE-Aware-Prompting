import html

# Example template for a blog post; it should contain `{title}` and `{body}` placeholders
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Render a blog entry safely for display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑escaped string ready for safe display.

    Raises
    ------
    ValueError
        If either `heading` or `content` is not a string.
    """
    if not isinstance(heading, str) or not isinstance(content, str):
        raise ValueError("Both heading and content must be strings.")

    # Escape special HTML characters to prevent XSS or markup injection
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Use the predefined format to assemble the final HTML
    formatted = BLOG_FORMAT.format(title=safe_heading, body=safe_content)

    return formatted.strip()