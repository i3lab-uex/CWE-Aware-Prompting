import html
from typing import Final

# Pre‑defined HTML template for a blog post. The placeholders `{title}` and `{body}`
# will be replaced with the sanitized values passed to `format_post_content`.
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe display on a webpage.

    Args:
        post_title: The headline or title of the blog post.
        post_body:  The full text content of the blog post.

    Returns:
        A string containing the sanitized, HTML‑formatted blog post.
    """
    # Escape any HTML special characters in title and body to prevent XSS attacks
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Return the fully formatted post using the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)