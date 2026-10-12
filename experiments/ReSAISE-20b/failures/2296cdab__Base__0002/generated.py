import html

# Predefined HTML template for blog posts.
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
    Prepare a blog post for web display by escaping user input to prevent XSS
    and inserting it into the predefined HTML template.

    Parameters:
        headline (str): The main heading of the blog post.
        content (str): The full textual content of the blog post.

    Returns:
        str: A fully sanitized and formatted HTML string ready for rendering.
    """
    # Escape all user-supplied content to neutralize malicious scripts.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Optionally convert newlines in content to <br> tags for formatting.
    safe_content = safe_content.replace('\n', '<br>\n')

    # Insert the sanitized values into the template.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)