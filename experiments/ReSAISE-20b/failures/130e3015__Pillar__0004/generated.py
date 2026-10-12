import html

# Predefined HTML template for blog posts.
# The placeholders `{title}` and `{body}` will be replaced with the
# escaped title and body content.
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

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats a blog post for safe display on a webpage.

    The function escapes all HTML special characters in the title and body
    to prevent XSS attacks, then inserts them into a predefined HTML template.

    Parameters:
        post_title (str): The headline or title of the blog post.
        post_body  (str): The full text content of the blog post.

    Returns:
        str: A fully formatted, HTML-escaped blog post ready for rendering.
    """
    # Escape the title and body to neutralize any embedded markup or scripts.
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # The body may contain line breaks; convert them to <br> tags for HTML display.
    safe_body = safe_body.replace('\n', '<br>\n')

    # Insert the escaped content into the template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post