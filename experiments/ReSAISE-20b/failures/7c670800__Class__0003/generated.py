import html

# Predefined template for a blog post. The placeholders are `{title}` and `{body}`.
BLOG_FORMAT = """
<article class="blog-post">
    <h2>{title}</h2>
    <div class="content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Safely formats a blog entry for display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑escaped string ready for safe rendering on a webpage.

    Raises
    ------
    ValueError
        If either heading or content is empty.
    """
    if not heading:
        raise ValueError("Heading must not be empty.")
    if content is None:  # allow empty content but disallow None
        raise ValueError("Content must not be None.")

    # Escape all user input to prevent XSS or injection via HTML
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Format the blog entry using the predefined template
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_entry