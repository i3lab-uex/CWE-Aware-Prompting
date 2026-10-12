import html

# Predefined template for a blog post.
BLOG_FORMAT = "<article><h1>{title}</h1><section>{body}</section></article>"

def display_blog_entry(heading: str, content: str) -> str:
    """
    Sanitize and format a blog entry for safe display on a webpage.

    Args:
        heading (str): The title of the blog post.
        content (str): The main text content of the blog post.

    Returns:
        str: A sanitized HTML string containing the formatted blog entry.
    """
    # Escape any potentially dangerous characters to prevent XSS or
    # HTML injection.  `html.escape` converts &, <, >, " and '.
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Render the template with the sanitized values.
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_entry