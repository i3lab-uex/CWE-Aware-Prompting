import html

# Pre‑defined HTML template with placeholders for title and body.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe HTML display.

    Args:
        post_title: The headline or title of the blog post.
        post_body:  The full text content of the blog post.

    Returns:
        A string containing a well‑formed HTML snippet ready for rendering.
    """
    # Escape any potentially malicious content to prevent XSS.
    safe_title = html.escape(post_title, quote=True)
    safe_body  = html.escape(post_body, quote=True)

    # Insert the sanitized values into the template.
    formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted