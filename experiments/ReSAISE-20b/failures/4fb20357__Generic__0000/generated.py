import html

# Predefined HTML template for a blog post. 
# `{title}` and `{body}` are placeholders that will be replaced by the sanitized
# heading and description respectively.
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

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.

    Notes
    -----
    * The function escapes all characters that have special meaning in HTML
      (e.g., <, >, &, ", ') to prevent cross‑site scripting attacks.
    * The returned string is safe for direct inclusion in an HTML page
      because no raw user input is rendered without escaping.
    """
    # Escape special characters to prevent XSS attacks
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(description, quote=True)

    # Replace placeholders in the template with the escaped values
    formatted_blog = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_blog