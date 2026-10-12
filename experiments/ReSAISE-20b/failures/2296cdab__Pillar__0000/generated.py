#!/usr/bin/env python3
"""
A helper for safely rendering user‑submitted blog posts into a pre‑defined HTML template.
"""

import html
from typing import Final

# A minimal but realistic blog format.  The placeholders {title} and {body}
# will be replaced by the sanitized headline and content.
BLOG_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
</body>
</html>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and embed a user‑supplied headline and content into the BLOG_FORMAT template.

    Parameters
    ----------
    headline : str
        The title of the blog post.  It will be HTML‑escaped to prevent injection.
    content : str
        The full body of the post.  It will be HTML‑escaped and then wrapped in a <p>
        tag for each paragraph.  Empty lines are treated as paragraph breaks.

    Returns
    -------
    str
        A complete HTML document ready to be served.  The string is fully escaped,
        preventing XSS and other injection attacks.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(content, str):
        raise TypeError(f"content must be a string, got {type(content).__name__}")

    # Escape headline and content to neutralise any HTML or script injection.
    safe_headline = html.escape(headline, quote=True)

    # Split content into paragraphs on double newlines.  Each paragraph is escaped
    # and wrapped in a <p> tag.  This keeps the visual structure of the original
    # text while ensuring safety.
    paragraphs = [
        f"<p>{html.escape(paragraph.strip(), quote=True)}</p>"
        for paragraph in content.splitlines()
        if paragraph.strip()  # ignore empty lines
    ]
    safe_body = "\n".join(paragraphs)

    # Render the final HTML using the template.
    rendered = BLOG_FORMAT.format(title=safe_headline, body=safe_body)

    # Basic sanity check: ensure placeholders have been replaced.
    if "{title}" in rendered or "{body}" in rendered:
        raise RuntimeError("Template placeholders were not fully replaced.")

    return rendered