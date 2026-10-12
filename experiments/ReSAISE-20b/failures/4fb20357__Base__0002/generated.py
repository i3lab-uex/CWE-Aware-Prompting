#!/usr/bin/env python3
"""
A utility to safely render a blog post for web display.

The function `display_blog` takes a heading and description, escapes any
HTML-sensitive characters to prevent XSS attacks (CWE‑79), then inserts the
cleaned content into a predefined HTML template.
"""

from html import escape

# Predefined HTML structure for a blog post
BLOG_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{heading}</title>
</head>
<body>
    <article>
        <h1>{heading}</h1>
        <div class="content">
            {description}
        </div>
    </article>
</body>
</html>
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
        A string containing the sanitized and HTML‑formatted blog post.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralise any characters that
      could be interpreted as HTML markup, thereby mitigating XSS risks.
    * Only the provided heading and description are inserted into the
      template; no other user input is included.
    """
    # Sanitize user input to prevent XSS
    safe_heading = escape(heading, quote=True)
    # Preserve line breaks in the description by converting newlines to <br>
    safe_description = escape(description, quote=True).replace("\n", "<br>")

    # Format the final HTML
    return BLOG_FORMAT.format(heading=safe_heading, description=safe_description)

# Example usage (commented out to avoid execution on import)
# if __name__ == "__main__":
#     h = "My <script>alert('XSS');</script> Post"
#     d = "Hello, world!\nThis is a test."
#     print(display_blog(h, d))