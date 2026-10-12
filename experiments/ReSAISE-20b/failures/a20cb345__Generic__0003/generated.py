import html
from typing import Final

# Example predefined template. In real use, this would be provided elsewhere.
BLOG_FORMAT: Final[str] = """
<article>
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a blog post for safe HTML display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post,
        ready for safe display in a browser.

    Raises
    ------
    ValueError
        If either `subject` or `description` is empty.
    """
    if not subject.strip():
        raise ValueError("Subject cannot be empty.")
    if not description.strip():
        raise ValueError("Description cannot be empty.")

    # Escape HTML special characters to prevent XSS
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Optionally, remove any remaining script tags or inline event handlers
    # (simple regex approach – for more robust sanitization, use a library)
    import re
    safe_body = re.sub(r'<\s*script[^>]*>(.*?)<\s*/\s*script\s*>', '', safe_body, flags=re.IGNORECASE | re.DOTALL)

    # Format using the predefined template
    formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted.strip()