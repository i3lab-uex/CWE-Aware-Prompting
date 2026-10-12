import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced by the
# escaped headline and text respectively.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Safely format and return a blog entry as an HTML string.

    Parameters
    ----------
    headline : str
        The title of the blog post. User supplied.
    text : str
        The full body content of the blog post. User supplied.

    Returns
    -------
    str
        An HTML string ready for inclusion in a webpage, with all user
        input properly escaped to prevent XSS attacks.

    Raises
    ------
    ValueError
        If either headline or text is not a string.
    """
    if not isinstance(headline, str) or not isinstance(text, str):
        raise ValueError("headline and text must be strings")

    # Escape user input to neutralise any embedded HTML/JS
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Insert the escaped values into the template
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_text)
    return formatted_post