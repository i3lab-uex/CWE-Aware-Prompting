#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility to assemble a safe, HTML‑formatted forum post.

The function `compile_post` takes a title, body text and a list of
discussion points (in markdown format) and returns an HTML string that
can be safely embedded in a web page or sent to another system.
All user supplied content is escaped to prevent HTML injection
(CWE‑74).
"""

import html
from typing import List

# --------------------------------------------------------------------------- #
# Configuration:  The HTML skeleton for a forum post.
#
# The placeholders are:
#   {title}   – escaped title of the post
#   {body}    – escaped body text, with line breaks converted to <br>
#   {points}  – an unordered list (<ul>) of discussion points
#
FORUM_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="post-body">
        {body}
    </section>
    <footer class="discussion-points">
        <h2>Discussion Points</h2>
        {points}
    </footer>
</article>
"""

# --------------------------------------------------------------------------- #
def _escape_markdown_list_items(items: List[str]) -> str:
    """
    Convert a list of markdown strings into an HTML <ul> string.

    Each item is escaped to neutralise special characters, then wrapped
    in <li> tags.  The function returns a single string containing the
    entire list.
    """
    escaped_items = [f"<li>{html.escape(item.strip())}</li>" for item in items]
    return "<ul>\n" + "\n".join(escaped_items) + "\n</ul>"

# --------------------------------------------------------------------------- #
def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given components.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.  Line breaks are
        preserved as <br> tags.
    highlights : List[str]
        A list of discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted, HTML‑escaped forum post string.
    """
    # 1. Sanitize title and body
    safe_title = html.escape(subject.strip())
    # Convert newlines to <br> tags for readability
    safe_body = html.escape(text.strip()).replace("\n", "<br>\n")

    # 2. Render discussion points as an unordered list
    safe_points = _escape_markdown_list_items(highlights)

    # 3. Populate the template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return post_html.strip()

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    title = "How to Secure Your Web App?"
    body = """Hello community,

I am looking for best practices on preventing XSS attacks.
Any suggestions?"""

    points = [
        "Use `html.escape()` for all user inputs.",
        "Implement Content Security Policy (CSP).",
        "<script>alert('test');</script> This is malicious code!"
    ]

    print(compile_post(title, body, points))