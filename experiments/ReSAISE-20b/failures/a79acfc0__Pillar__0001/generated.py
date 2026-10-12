import html
from typing import Final

# Template for rendering a blog post. The placeholders are safe because we escape
# the user supplied values before inserting them.
BLOG_FORMAT: Final[str] = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">{body}</div>\n"
    "</article>"
)

def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post for safe display on a web page.

    Parameters
    ----------
    title : str
        The user‑supplied title of the blog post.
    body : str
        The user‑supplied main content of the blog post.

    Returns
    -------
    str
        The fully rendered HTML string with user content safely escaped.
    
    Raises
    ------
    ValueError
        If either title or body is empty or exceeds 10,000 characters.
    
    Notes
    -----
    * The function uses :func:`html.escape` to neutralise any HTML, JavaScript or
      other markup that might be injected by a malicious user.
    * The rendering template is a constant string; no dynamic formatting
      beyond the safe placeholders is performed, mitigating CWE‑707 risks.
    """
    # Basic validation to avoid rendering nonsense or excessively large content
    if not title.strip():
        raise ValueError("Title must not be empty.")
    if not body.strip():
        raise ValueError("Body must not be empty.")

    # Optional: limit size to prevent DoS or excessive memory usage
    MAX_LENGTH = 10_000
    if len(title) > MAX_LENGTH or len(body) > MAX_LENGTH:
        raise ValueError(f"Title and body must not exceed {MAX_LENGTH} characters.")

    # Escape user input to neutralise HTML/JS injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the template with sanitized values
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return rendered