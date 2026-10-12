# SPDX-License-Identifier: MIT
"""
Utility for safely rendering a user‑submitted blog post.

The function sanitises the headline and body text by escaping HTML
special characters, preventing cross‑site scripting (XSS) or injection
issues.  The formatted post is returned as a plain string ready for
embedding in an HTML page.

CWE‑74 (Injection) mitigated by proper escaping of user input.
"""

from html import escape
import re

# Example template; in a real application this would be defined elsewhere.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def _remove_script_tags(text: str) -> str:
    """
    Remove any <script>...</script> blocks to avoid JavaScript injection.
    This is a defensive step; the primary protection comes from escaping.
    """
    script_pattern = re.compile(r"<script\b[^>]*>(.*?)</script>", flags=re.IGNORECASE | re.DOTALL)
    return script_pattern.sub("", text)

def show_blog_post(headline: str, text: str) -> str:
    """
    Render a blog post safely.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The body content of the blog post.

    Returns
    -------
    str
        A sanitized, formatted HTML snippet containing the post.
    """
    # Defensive: strip script tags first
    safe_headline = _remove_script_tags(headline)
    safe_text = _remove_script_tags(text)

    # Escape all special HTML characters
    escaped_headline = escape(safe_headline, quote=True)
    escaped_text = escape(safe_text, quote=True)

    # Format the post using the predefined template
    formatted_post = BLOG_FORMAT.format(title=escaped_headline, body=escaped_text)

    return formatted_post