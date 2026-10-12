import html

# Predefined HTML template for blog posts.
# Placeholders: {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats and sanitizes a blog post for safe HTML display.

    Args:
        post_title (str): The headline or title of the blog post.
        post_body  (str): The full text content of the blog post.

    Returns:
        str: A fully formatted HTML string safe for rendering in a browser.
    """
    # Escape special characters to prevent XSS and HTML injection
    safe_title = html.escape(post_title, quote=True)
    safe_body  = html.escape(post_body, quote=True)

    # Insert the sanitized content into the template
    formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted.strip()