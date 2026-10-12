import html

# Predefined HTML structure with placeholders for title and body.
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
    Prepare a user‑submitted blog post for safe HTML display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Escape special HTML characters to prevent injection attacks.
    safe_title = html.escape(heading, quote=True)
    # Preserve line breaks in the body by converting newlines to <br>.
    safe_body = html.escape(description, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)