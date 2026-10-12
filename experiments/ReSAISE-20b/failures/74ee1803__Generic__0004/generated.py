import html

# Predefined HTML template for blog posts. The placeholders {title} and {body}
# will be replaced by the sanitized headline and text respectively.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and sanitize a blog entry for safe HTML display.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized, HTML-formatted blog post.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape HTML special characters to prevent XSS attacks.
    safe_headline = html.escape(headline, quote=True)
    # Preserve line breaks in the body by converting newlines to <br>.
    safe_body = html.escape(text, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_headline, body=safe_body)