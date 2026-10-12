import html

# Predefined HTML structure with placeholders for title and body.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and format a blog entry for safe HTML display.

    Args:
        headline (str): The main heading of the blog post.
        content (str): The full textual content of the blog post.

    Returns:
        str: A complete HTML snippet ready for rendering on a webpage.
    """
    # Escape any special HTML characters to prevent injection attacks
    safe_title = html.escape(headline, quote=True)
    # Preserve line breaks in the content by converting them to <br> tags
    escaped_content = html.escape(content, quote=True).replace("\n", "<br>")
    
    # Populate the predefined template with sanitized data
    return BLOG_FORMAT.format(title=safe_title, body=escaped_content)