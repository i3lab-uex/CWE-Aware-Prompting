import html
from typing import Any

# Example template; in real use this would be defined elsewhere
BLOG_FORMAT: str = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"post-body\">{body}</div>\n"
    "</article>"
)

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely for web display.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string containing the formatted blog post.

    Raises
    ------
    TypeError
        If either ``title`` or ``body`` is not a string.
    ValueError
        If the rendered output would contain malformed HTML due to injection attempts.

    Notes
    -----
    * Uses :func:`html.escape` to neutralize any HTML or JavaScript that a user might
      attempt to inject.
    * Performs basic type checks to guard against improper inputs that could break the
      template rendering (CWE-707).
    """
    # Basic type validation to avoid malformed messages
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(body, str):
        raise TypeError(f"body must be a string, got {type(body).__name__}")

    # Escape user input to neutralize any embedded markup
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the template
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    # Quick sanity check: ensure no unescaped tags remain
    if "<" in safe_title or ">" in safe_body:
        # This should never happen due to escape, but guard against it
        raise ValueError("Rendered content contains unexpected tags")

    return rendered