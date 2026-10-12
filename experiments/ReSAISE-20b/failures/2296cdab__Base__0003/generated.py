import html

# Predefined HTML structure for a blog post.  It contains two placeholders:
#   {title}   – where the headline will be inserted
#   {body}    – where the main content will be inserted
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
    Prepare a user‑submitted blog entry for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.

    Notes
    -----
    - The function escapes all characters that have special meaning in HTML
      (e.g. <, >, &, ", ') to prevent cross‑site scripting (CWE‑79).
    - The escaped values are then inserted into the predefined `BLOG_FORMAT`
      template.
    """
    # Escape headline and content to neutralize any HTML or JavaScript
    safe_headline = html.escape(headline, quote=True)
    # For content we also escape; if you want to allow simple line breaks,
    # convert newlines to <br> after escaping.
    safe_content = html.escape(content, quote=True).replace('\n', '<br>\n')

    # Format the final HTML using the template
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)