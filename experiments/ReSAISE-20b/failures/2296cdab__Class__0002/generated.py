import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and format a blog post for safe HTML display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on a webpage.

    Raises
    ------
    ValueError
        If either headline or content is empty.
    """
    if not headline:
        raise ValueError("Headline cannot be empty.")
    if not content:
        raise ValueError("Content cannot be empty.")

    # Escape special HTML characters to prevent injection (CWE-74).
    safe_title = html.escape(headline, quote=True)
    # Preserve line breaks in the content by converting them to <br>.
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)