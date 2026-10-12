#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that builds a safe, formatted forum post from user supplied content.
"""

from __future__ import annotations

import html
from typing import Iterable, List

# --------------------------------------------------------------------------- #
#   Configuration
# --------------------------------------------------------------------------- #

#: Template for the forum post.  The placeholders are used by
#: :func:`construct_forum_content`.
FORUM_POST_FORMAT: str = (
    "<h1>{header}</h1>\n"
    "<div>{message}</div>\n"
    "<ul>{options}</ul>"
)

# --------------------------------------------------------------------------- #
#   Public API
# --------------------------------------------------------------------------- #

def construct_forum_content(
    heading: str,
    content: str,
    choices: Iterable[str],
) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body of the post.  Any HTML special characters are escaped.
    choices : Iterable[str]
        A collection of user‑supplied options.  Each option is escaped
        and rendered as an HTML list item.

    Returns
    -------
    str
        A complete, safe forum post ready to be inserted into a web page.

    Raises
    ------
    TypeError
        If ``choices`` is not an iterable of strings.
    """
    # Validate that we received an iterable of strings
    if not isinstance(choices, Iterable):
        raise TypeError("`choices` must be an iterable of strings")

    # Escape heading and content to prevent XSS
    safe_heading = html.escape(str(heading), quote=True)
    safe_content = html.escape(str(content), quote=True)

    # Convert each choice to a safe <li> element
    li_items: List[str] = []
    for idx, choice in enumerate(choices):
        if not isinstance(choice, str):
            raise TypeError(f"choice at index {idx} is not a string")
        safe_choice = html.escape(choice, quote=True)
        li_items.append(f"<li>{safe_choice}</li>")

    # Join the list items into a single string
    options_html = "\n".join(li_items)

    # Render the final post using the template
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html,
    )

# --------------------------------------------------------------------------- #
#   Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     post = construct_forum_content(
#         heading="Upcoming Features",
#         content="Please choose which feature you'd like to see first.",
#         choices=[
#             "Real‑time analytics",
#             "Improved UI themes",
#             "Advanced filtering options"
#         ]
#     )
#     print(post)