# -*- coding: utf-8 -*-
"""
Utility to generate a safe HTML representation of a forum post.
"""

from html import escape
from typing import List

# Example template; in real usage this should be defined elsewhere.
USER_POST_FORMAT: str = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author_name}</p>
    <div class="content">{content}</div>
    <div class="tags">{tags}</div>
</div>
"""

def create_post_html(
    author_name: str,
    post_title: str,
    content: str,
    post_tags: List[str]
) -> str:
    """
    Construct an XSS‑protected HTML snippet for a forum post.

    Parameters
    ----------
    author_name : str
        Name of the user who authored the post.
    post_title : str
        Title (headline) of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A string containing the formatted, escaped HTML representation of the post.
    """
    # Escape all user supplied strings to prevent XSS
    safe_author = escape(author_name, quote=True)
    safe_title = escape(post_title, quote=True)
    safe_content = escape(content)

    # Build the tags HTML; each tag is wrapped in a <span>
    safe_tags = "".join(
        f'<span class="tag">{escape(tag, quote=True)}</span>' for tag in post_tags
    )

    # Format the final HTML using the predefined template
    html_output = USER_POST_FORMAT.format(
        title=safe_title,
        author_name=safe_author,
        content=safe_content,
        tags=safe_tags
    )
    return html_output.strip()