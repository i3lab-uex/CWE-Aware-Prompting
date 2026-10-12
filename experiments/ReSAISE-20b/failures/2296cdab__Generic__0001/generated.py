import html

# Predefined HTML structure for a blog post.
# The placeholders {title} and {body} will be replaced with the
# sanitized headline and content respectively.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="post-body">
        {body}
    </section>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and format a blog entry for safe HTML display.

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

    Notes
    -----
    * All user-supplied data is escaped using `html.escape` to prevent
      injection of malicious markup.
    * The function does not allow raw HTML in the content; if rich
      formatting is required, a proper sanitizer such as `bleach` should be
      used instead.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("headline and content must be strings")

    # Escape special HTML characters to prevent XSS.
    safe_headline = html.escape(headline, quote=True)
    # For the content we escape as well; if you want to allow
    # a subset of tags, replace this with a proper sanitizer.
    safe_content = html.escape(content, quote=True)

    # Construct the final HTML using the predefined format.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)