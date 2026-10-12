import html

# Example HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with the sanitized values.
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

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe HTML display.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A fully-formed, sanitized HTML string ready to be inserted into a page.

    Raises
    ------
    ValueError
        If either `post_title` or `post_body` is not a string.
    """
    if not isinstance(post_title, str) or not isinstance(post_body, str):
        raise ValueError("Both post_title and post_body must be strings.")

    # Escape HTML special characters to prevent XSS.
    safe_title = html.escape(post_title, quote=True)
    # For the body we also escape but preserve line breaks by converting \n to <br>.
    safe_body = html.escape(post_body, quote=True).replace("\n", "<br>")

    # Format the final HTML.
    try:
        formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    except KeyError as exc:
        raise ValueError(f"Invalid placeholder in BLOG_FORMAT: {exc}") from exc

    return formatted