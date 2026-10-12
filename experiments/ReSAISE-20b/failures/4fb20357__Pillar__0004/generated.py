#!/usr/bin/env python3
"""
Utility to safely format a blog post for web display.
"""

from html import escape
import re

# A minimal but realistic HTML template.  The placeholders `{title}` and `{body}`
# are replaced with the sanitized heading and description.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="post-content">
        {body}
    </section>
</article>
"""

# Regular expression to strip any existing HTML tags that might have been
# inadvertently included by the user.  This is an extra safety layer.
TAG_RE = re.compile(r'<[^>]+>')


def _sanitize(text: str) -> str:
    """
    Escapes special HTML characters and removes any stray tags.
    """
    # First escape &, <, >, ", '
    escaped = escape(text, quote=True)
    # Then remove any tags that might have slipped through
    cleaned = TAG_RE.sub('', escaped)
    return cleaned


def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe HTML rendering.

    Parameters
    ----------
    heading : str
        The main title of the blog post.
    description : str
        The full body text of the blog post.

    Returns
    -------
    str
        A complete HTML snippet ready to be embedded in a page.

    Raises
    ------
    ValueError
        If either argument is not a string.
    """
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(description, str):
        raise ValueError("description must be a string")

    safe_title = _sanitize(heading)
    safe_body = _sanitize(description)

    # Use str.format with explicit placeholders to avoid accidental injection.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)