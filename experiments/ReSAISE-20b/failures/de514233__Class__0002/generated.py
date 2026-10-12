import html

# Predefined template for blog posts.
BLOG_FORMAT = """
<article>
    <h1>{title}</h1>
    <div class="content">
        {body}
    </div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Render a user‑submitted blog post safely for display in HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post ready for safe display.

    Raises
    ------
    ValueError
        If either `headline` or `text` is not a string.
    """
    # Validate input types
    if not isinstance(headline, str):
        raise ValueError("headline must be a string")
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    # Escape special HTML characters to prevent injection attacks (CWE‑74)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Construct the final output
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_text)

    return formatted_post