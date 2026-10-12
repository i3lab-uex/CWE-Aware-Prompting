import html

# Predefined HTML template for blog posts.
# The placeholders {title} and {body} will be replaced with the
# sanitized heading and description respectively.
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

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main headline of the blog post.
    description : str
        The full textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for insertion into a web page.

    Raises
    ------
    ValueError
        If either ``heading`` or ``description`` is not a string.
    """
    if not isinstance(heading, str) or not isinstance(description, str):
        raise ValueError("Both heading and description must be strings")

    # Escape all characters that could create HTML or JavaScript payloads.
    safe_title = html.escape(heading, quote=True)
    # For the body we allow line breaks to be preserved by converting
    # newline characters to <br> tags after escaping.
    escaped_body = html.escape(description, quote=True).replace('\n', '<br>')

    # Ensure the final HTML is well‑formed by substituting placeholders.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=escaped_body)

    return formatted_post