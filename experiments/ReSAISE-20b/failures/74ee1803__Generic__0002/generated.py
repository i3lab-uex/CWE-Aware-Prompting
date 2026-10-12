import html

# Example template (this should be defined elsewhere in the real application)
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{headline}</h1>
  <div class="post-content">{text}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Safely format a blog post for display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full content of the blog post.

    Returns
    -------
    str
        An HTML string with the headline and text inserted into BLOG_FORMAT,
        after escaping any potentially harmful characters.
    """
    # Escape user-supplied content to prevent XSS
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Format the final HTML
    return BLOG_FORMAT.format(headline=safe_headline, text=safe_text)