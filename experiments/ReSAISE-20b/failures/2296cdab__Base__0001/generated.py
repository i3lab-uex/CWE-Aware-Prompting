import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and format a blog entry for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        An HTML string with the sanitized headline and body, ready for inclusion in a web page.

    Notes
    -----
    * Uses `html.escape` to neutralize any potentially malicious HTML or JavaScript.
    * Preserves line breaks by converting newline characters to `<br>` tags.
    """
    # Escape HTML special characters in headline and content
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Convert line breaks to <br> tags for the body
    safe_content = safe_content.replace('\n', '<br>\n')

    # Populate the predefined format
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_content)

    return formatted_post