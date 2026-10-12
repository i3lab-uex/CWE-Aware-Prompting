#!/usr/bin/env python3
"""
Utility to build a sanitized HTML representation of a forum post.
"""

import html
from typing import List

# Predefined template for the post.  The ``{tags}`` placeholder will be replaced
# with a string containing <span> elements for each tag.
USER_POST_FORMAT: str = (
    "<div class='post'>"
    "  <h2>{post_heading}</h2>"
    "  <p class='author'>by {user_name}</p>"
    "  <div class='content'>{post_content}</div>"
    "  <div class='tags'>{tags}</div>"
    "</div>"
)


def _validate_tags(tags: List[str]) -> None:
    """
    Ensure that ``tags`` is a list of strings.
    Raises a TypeError if the check fails.
    """
    if not isinstance(tags, list):
        raise TypeError("post_tags must be a list of strings")
    for tag in tags:
        if not isinstance(tag, str):
            raise TypeError("Each tag must be a string")


def build_post_html(
    user_name: str,
    post_heading: str,
    post_content: str,
    post_tags: List[str],
) -> str:
    """
    Build a sanitized HTML string for a forum post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        The title of the user's post.
    post_content : str
        The main content of the user's post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A sanitized HTML representation of the user's post.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Validate input types
    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")
    if not isinstance(post_heading, str):
        raise TypeError("post_heading must be a string")
    if not isinstance(post_content, str):
        raise TypeError("post_content must be a string")
    _validate_tags(post_tags)

    # Escape all user-supplied content to avoid XSS
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(post_content, quote=False)

    # Build the tags string: each tag is wrapped in a <span>
    safe_tags = ""
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags += f"<span class='tag'>{escaped_tag}</span>"

    # Format the final HTML
    html_output = USER_POST_FORMAT.format(
        post_heading=safe_heading,
        user_name=safe_user_name,
        post_content=safe_content,
        tags=safe_tags,
    )
    return html_output