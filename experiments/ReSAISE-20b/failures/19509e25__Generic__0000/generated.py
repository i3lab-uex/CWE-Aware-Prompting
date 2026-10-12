# -*- coding: utf-8 -*-

import html
from typing import List

# Example template – in real use this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
    <h2>{headline}</h2>
    <p class="author">Posted by: {poster_name}</p>
    <div class="content">{text}</div>
    <div class="tags">{tags}</div>
</div>
"""

def compose_post_html(
    poster_name: str,
    headline: str,
    text: str,
    hashtags: List[str]
) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        The name of the author.
    headline : str
        The post's title.
    text : str
        The main body of the post.
    hashtags : list[str]
        A list of tags to be displayed.

    Returns
    -------
    str
        Escaped HTML string following the USER_POST_FORMAT template.
    """
    # Escape all user‑supplied content
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline   = html.escape(headline, quote=True)
    safe_text       = html.escape(text, quote=False)  # preserve line breaks if needed

    # Build tags: each tag wrapped in <span>, escape the tag text
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    ]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )