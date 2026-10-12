import html

# Predefined HTML structure for a blog post.  
# {{title}} and {{body}} are placeholders that will be replaced with sanitized content.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{{title}}</h1>
    </header>
    <section class="content">
        {{body}}
    </section>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.
    """
    # Escape any HTML special characters to prevent XSS or injection attacks
    safe_heading = html.escape(heading, quote=True)
    # Preserve line breaks in the body by converting them to <br> tags
    safe_body = html.escape(text, quote=True).replace('\n', '<br>\n')

    # Construct the final HTML by replacing placeholders
    formatted_post = BLOG_FORMAT.replace('{{title}}', safe_heading).replace(
        '{{body}}', safe_body
    )

    return formatted_post