import html

# Predefined HTML structure for a blog post.  
# It contains two placeholders: {title} and {body}.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        An HTML string with the headline and content safely escaped.
    """
    # 1. Escape user input to neutralize special characters that could
    #    be interpreted as HTML or script.  This protects against CWE‑74.
    safe_headline = html.escape(headline, quote=True)
    # For the body we allow basic paragraph tags but still escape other
    # special characters.  If richer formatting is required, a
    # dedicated sanitiser should be used.
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    # 2. Insert the sanitized values into the predefined template.
    formatted = BLOG_FORMAT.format(title=safe_headline, body=safe_body)

    return formatted