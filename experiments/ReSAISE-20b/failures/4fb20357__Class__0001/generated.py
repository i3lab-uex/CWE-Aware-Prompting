import html

# Predefined HTML structure for a blog post.
# The placeholders {title} and {body} will be replaced with the escaped content.
BLOG_FORMAT: str = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe HTML rendering.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post.

    Raises
    ------
    TypeError
        If either ``heading`` or ``description`` is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError(f"Expected heading to be a string, got {type(heading).__name__}")
    if not isinstance(description, str):
        raise TypeError(f"Expected description to be a string, got {type(description).__name__}")

    # Escape special HTML characters to prevent injection (CWE‑74).
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Insert the escaped content into the predefined format.
    return BLOG_FORMAT.format(title=safe_heading, body=safe_description)