import html

# Predefined HTML template for a blog post.
# It expects two placeholders: {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Prepare a user-submitted blog post for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML-formatted string ready for rendering.
    """
    # Sanitize the headline: escape special HTML characters
    safe_headline = html.escape(headline, quote=True)

    # Sanitize the content: escape special HTML characters
    escaped_content = html.escape(content, quote=True)

    # Preserve line breaks by converting newline characters to <br>
    safe_body = escaped_content.replace('\n', '<br>\n')

    # Render the final HTML using the predefined template
    return BLOG_FORMAT.format(title=safe_headline, body=safe_body)