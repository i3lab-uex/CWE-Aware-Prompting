# -*- coding: utf-8 -*-
"""
Secure rendering of a user's forum post.

The `render_user_content` function accepts user-provided data and safely escapes it
before inserting it into a predefined HTML template.  This prevents Cross‑Site
Scripting (XSS) attacks by ensuring that any HTML or JavaScript in the input is
rendered as plain text rather than executable code.

The module relies only on Python's standard library (`html.escape`) and therefore
has no external dependencies.
"""

import html
from typing import List

# Example template.  In a real application this would be imported from a
# configuration module or defined elsewhere.
USER_POST_FORMAT: str = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {username}</p>
    <div class="content">{body}</div>
    <div class="tags">
        {tags}
    </div>
</div>
"""


def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str],
) -> str:
    """
    Render a user's forum post into safe HTML.

    Parameters
    ----------
    username_key : str
        The identifier of the post's creator.
    title_key : str
        The heading of the user's post.
    body_key : str
        The primary content of the user's post.
    tag_elements : list[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        An XSS‑protected HTML representation of the user's forum post.

    Notes
    -----
    * All user‑supplied strings are escaped using ``html.escape``.
    * Each tag is wrapped in a `<span>` element and the resulting string
      inserted into the template.
    """
    # Escape user-provided strings to neutralise any embedded HTML/JS
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=False)  # body may contain line breaks

    # Build the tags string: each tag is wrapped in <span> and escaped
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    )

    # Render the final HTML using the template
    rendered_html = USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tags=safe_tags,
    )

    return rendered_html