import html

# Predefined HTML structure for blog posts with placeholders
BLOG_FORMAT = """
<div class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</div>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and format a blog post for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on the webpage.

    Raises
    ------
    ValueError
        If either `headline` or `content` is empty after stripping.
    """
    # Validate inputs
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("Both headline and content must be strings.")

    # Strip leading/trailing whitespace
    cleaned_headline = headline.strip()
    cleaned_content = content.strip()

    if not cleaned_headline:
        raise ValueError("Headline cannot be empty.")
    if not cleaned_content:
        raise ValueError("Content cannot be empty.")

    # Escape HTML special characters to prevent XSS
    escaped_headline = html.escape(cleaned_headline, quote=True)
    escaped_content = html.escape(cleaned_content, quote=True)

    # Replace newlines with <br> for proper HTML formatting
    formatted_body = escaped_content.replace("\n", "<br>\n")

    # Construct final HTML using the template
    formatted_post = BLOG_FORMAT.format(title=escaped_headline, body=formatted_body)

    return formatted_post