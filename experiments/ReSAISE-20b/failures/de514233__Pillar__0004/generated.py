import html
from string import Template

# Predefined template for blog posts.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>$title</h1>
    <div class="content">$body</div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        A string containing the HTML snippet for the blog post,
        with all user supplied content properly escaped.

    Raises
    ------
    ValueError
        If the title or body contains characters that would break the
        template (e.g., unescaped '$' signs).  The function escapes all
        user input, so this exception should not normally occur.
    """
    # Escape user supplied content to avoid XSS and other injection issues.
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Use Template to safely substitute placeholders.
    try:
        template = Template(BLOG_FORMAT)
        formatted_post = template.substitute(title=safe_title, body=safe_body)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in BLOG_FORMAT: {exc}") from exc
    except ValueError as exc:
        # Template will raise ValueError if there's an unescaped '$' in user data.
        raise ValueError("User input contains invalid characters for template substitution.") from exc

    return formatted_post