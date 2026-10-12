# -*- coding: utf-8 -*-

"""
A small utility to safely publish a blog article.
"""

import html

# A simple template with placeholders for title and body.
BLOG_FORMAT = """
<article>
  <h1>{title}</h1>
  <div class="content">
    {body}
  </div>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Render a blog article safely for display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A sanitized and formatted HTML string ready for safe display.
    """
    # Validate arguments are strings
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Escape HTML to prevent XSS attacks
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Format using the predefined template
    formatted_article = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_article