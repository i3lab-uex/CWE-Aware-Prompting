# -*- coding: utf-8 -*-
"""
Utility to build a safe, structured forum post.

The function `compile_post` accepts a title, body text and a list of
discussion points (in markdown).  It converts the markdown to HTML,
escapes any unsafe characters, and embeds everything into a
pre‑defined template.

Security considerations:
- All user supplied content is HTML escaped before rendering.
- The markdown conversion uses a limited set of extensions and the
  output is filtered by `bleach` to avoid XSS or other injection attacks.
- The function does not trust any part of the input; it treats it as
  untrusted data.

CWE-707: Improper Neutralization of Structured Data is mitigated by
sanitizing the rendered HTML with `bleach.clean` before it reaches the
client.
"""

import re
from typing import List

# External dependencies:
#   pip install markdown==3.6 bleach==5.0.1
import markdown  # type: ignore
import bleach     # type: ignore

# Allowed tags and attributes for the final HTML output.
ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
    "p", "ul", "ol", "li", "strong", "em", "code", "pre",
    "blockquote", "br"
]
ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "code": ["class"],
}
# Allowed protocols for links and images.
ALLOWED_PROTOCOLS = bleach.sanitizer.ALLOWED_PROTOCOLS + ["mailto"]

# Pre‑defined template for a forum post.
FORUM_POST_FORMAT = """
<h1>{title}</h1>
<div class="post-body">
{content}
</div>
<ul class="discussion-points">
{points}
</ul>
"""

def _escape_and_markdown(text: str) -> str:
    """
    Convert a markdown string to safe HTML.

    1. Escape any raw HTML tags in the input.
    2. Convert markdown to HTML using a limited set of extensions.
    3. Clean the result with bleach to remove disallowed tags/attributes.

    Parameters
    ----------
    text : str
        Raw markdown input.

    Returns
    -------
    str
        Sanitized HTML fragment.
    """
    # Step 1: Escape raw HTML to avoid injection.
    escaped = bleach.clean(text, tags=[], attributes={}, protocols=[])
    # Step 2: Convert markdown to HTML.
    md_html = markdown.markdown(
        escaped,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    # Step 3: Clean the resulting HTML.
    safe_html = bleach.clean(
        md_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
    )
    return safe_html

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a structured forum post.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized forum post as an HTML string.

    Raises
    ------
    ValueError
        If any of the inputs are not strings or the list contains non-string items.
    """
    # Input validation
    if not isinstance(subject, str):
        raise ValueError("subject must be a string")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(highlights, list) or any(not isinstance(h, str) for h in highlights):
        raise ValueError("highlights must be a list of strings")

    # Sanitize the title (escape but do not convert markdown).
    safe_title = bleach.clean(subject, tags=[], attributes={}, protocols=[])

    # Convert the main content to safe HTML.
    safe_content = _escape_and_markdown(text)

    # Build the list of discussion points.
    point_items = []
    for idx, h in enumerate(highlights, start=1):
        # Convert each highlight to safe HTML.
        safe_point = _escape_and_markdown(h)
        point_items.append(f"<li>{safe_point}</li>")

    safe_points = "\n".join(point_items)

    # Render the final template.
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        content=safe_content,
        points=safe_points
    )

    # Final cleanup to ensure no stray tags slip through.
    final_html = bleach.clean(
        post_html,
        tags=ALLOWED_TAGS + ["h1", "div", "ul"],
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
    )

    return final_html