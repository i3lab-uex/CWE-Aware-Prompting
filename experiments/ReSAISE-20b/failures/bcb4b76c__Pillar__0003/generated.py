#!/usr/bin/env python3
"""
create_forum_post – build a safe, well‑formed HTML forum post.

The function escapes user supplied content to prevent XSS and
CWE‑707 (improper neutralization of structured messages).
"""

from __future__ import annotations

import html
from typing import List

# Predefined HTML template. Placeholders: {title}, {body}, {points}
FORUM_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h2>{title}</h2>
  </header>
  <section class="post-body">
    {body}
  </section>
  <footer class="discussion-points">
    <h3>Discussion Points</h3>
    {points}
  </footer>
</article>
"""

def _escape_markdown(md: str) -> str:
    """
    Very lightweight markdown to HTML conversion with escaping.
    Only supports plain text; complex Markdown is rendered as escaped
    text to avoid injection.  This mitigates CWE‑707 by ensuring
    structured data remains well‑formed.
    """
    # Escape HTML special chars first
    escaped = html.escape(md)
    # Convert simple markdown list items to <li>
    lines = []
    for line in escaped.splitlines():
        if line.strip().startswith("- "):
            content = line.strip()[2:].strip()
            lines.append(f"<li>{content}</li>")
        else:
            # Preserve paragraphs
            lines.append(f"<p>{line.strip()}</p>")
    return "\n".join(lines)

def create_forum_post(topic: str, text_body: str, points: List[str]) -> str:
    """
    Build a sanitized HTML forum post.

    Args:
        topic: Title or main topic of the post.
        text_body: Main content of the post (plain text).
        points: List of discussion points in Markdown format.

    Returns:
        A string containing the fully formatted and sanitized HTML.
    """
    # Escape all user input
    safe_title = html.escape(topic)
    safe_body = _escape_markdown(text_body)

    # Build the unordered list for discussion points
    if not points:
        safe_points = "<p>No discussion points provided.</p>"
    else:
        list_items = []
        for point in points:
            # Each point may contain Markdown; convert safely
            safe_point = _escape_markdown(point)
            list_items.append(f"<li>{safe_point}</li>")
        safe_points = f"\n<ul>\n{''.join(list_items)}\n</ul>"

    # Format the final HTML
    html_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return html_post.strip()