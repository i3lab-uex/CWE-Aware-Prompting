import html

# Example template; in real usage this would be defined elsewhere.
BLOG_FORMAT = """
<article>
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

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
        A string containing the sanitized and formatted HTML of the post.
    """
    if not isinstance(headline, str) or not isinstance(text, str):
        raise TypeError("headline and text must be strings")

    # Escape HTML to prevent XSS attacks
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Format using the predefined template
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_text)

    return formatted_post