import html
from typing import Final

# Predefined template for blog posts. Adjust as needed.
BLOG_FORMAT: Final[str] = """
<div class="blog-post">
    <h2>{title}</h2>
    <div class="content">{body}</div>
</div>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Sanitize and format a blog post for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML for the blog post.

    Raises
    ------
    ValueError
        If either heading or content is empty after stripping whitespace.
    """
    # Validate input
    if not heading.strip():
        raise ValueError("Heading must not be empty.")
    if not content.strip():
        raise ValueError("Content must not be empty.")

    # Escape special HTML characters to prevent XSS
    safe_title = html.escape(heading, quote=True)
    # Preserve line breaks in content and escape HTML
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    # Format using the predefined template
    formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted.strip()