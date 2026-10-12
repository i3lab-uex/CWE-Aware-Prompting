import html

# Predefined HTML structure for a blog post with placeholders
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main headline or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML-formatted blog post ready for rendering.

    Raises
    ------
    TypeError
        If either heading or text is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape any special HTML characters to prevent injection attacks
    safe_title = html.escape(heading, quote=True)
    # For the body we also escape but preserve newlines as <br> for readability
    safe_body = html.escape(text, quote=True).replace('\n', '<br>')

    # Construct the final HTML using the predefined format
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post