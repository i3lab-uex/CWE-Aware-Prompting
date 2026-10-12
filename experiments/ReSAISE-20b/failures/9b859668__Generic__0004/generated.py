#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Forum post construction utility.

This module defines a single public function, `construct_forum_content`,
which safely formats user supplied content into an HTML forum post.
"""

from __future__ import annotations

import html
from typing import Iterable, List

# Default format string for the forum post.
# It expects three placeholders: {header}, {message} and {options}.
FORUM_POST_FORMAT = (
    "<div class=\"forum-post\">\n"
    "  <h2>{header}</h2>\n"
    "  <div class=\"post-body\">{message}</div>\n"
    "  {options}\n"
    "</div>"
)


def _escape_markdown(text: str) -> str:
    """
    Escape HTML special characters in a Markdown string.

    Parameters
    ----------
    text : str
        The raw Markdown input from the user.

    Returns
    -------
    str
        The escaped string safe for embedding in HTML.
    """
    return html.escape(text, quote=True)


def _build_options_list(choices: Iterable[str]) -> str:
    """
    Convert a collection of Markdown strings into an HTML unordered list.

    Parameters
    ----------
    choices : Iterable[str]
        The user supplied options in Markdown format.

    Returns
    -------
    str
        A string containing a safe `<ul>` element with each option as an `<li>`.
    """
    if not any(choices):
        return ""  # No options to display

    list_items = []
    for choice in choices:
        escaped_choice = _escape_markdown(choice)
        list_items.append(f"<li>{escaped_choice}</li>")

    return "<ul>\n" + "\n".join(list_items) + "\n</ul>"


def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str],
) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post (Markdown allowed).
    choices : List[str]
        A list of user-provided options or discussion points in Markdown format.

    Returns
    -------
    str
        A fully formatted HTML string representing the forum post.
    """
    # Sanitize inputs
    safe_heading = _escape_markdown(heading)
    safe_content = _escape_markdown(content)

    # Build options list
    options_html = _build_options_list(choices)

    # Format the final post using the predefined template
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html,
    )