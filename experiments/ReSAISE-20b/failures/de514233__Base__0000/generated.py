import html

# Example template – in real use this should be defined elsewhere
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
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the escaped title and body inserted into BLOG_FORMAT.
    """
    # Ensure inputs are strings
    if headline is None:
        headline = ""
    if text is None:
        text = ""

    # Escape user input to prevent XSS (CWE-79)
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the post using the predefined template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post