import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats and sanitizes a user‑submitted blog post for safe display on a webpage.

    Args:
        post_title (str): The headline or title of the blog post.
        post_body (str): The full text content of the blog post.

    Returns:
        str: A fully sanitized HTML string ready for rendering.
    """
    # Escape special HTML characters to prevent XSS and ensure well‑formedness.
    safe_title = html.escape(post_title, quote=True)
    safe_body  = html.escape(post_body, quote=True)

    # Construct the final HTML using the predefined template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post