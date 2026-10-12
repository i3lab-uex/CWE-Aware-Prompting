# -*- coding: utf-8 -*-
"""
Utility for rendering a user profile safely for web display.
"""

import html
from typing import Any

# Example template – in real usage this would be defined elsewhere.
PROFILE_FORMAT: str = (
    "<div class=\"profile\">\n"
    "  <h1>{fullname}</h1>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <div class=\"status\">{current_status}</div>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user profile for web display, ensuring all content is safely escaped.

    Args:
        fullname (str): The user's name as entered.
        biography (str): A user-written biography that may span multiple sentences.
        current_status (str): A brief, current status message.

    Returns:
        str: A formatted HTML string containing the sanitized profile information.

    Raises:
        TypeError: If any argument is not a string.
    """
    # Validate input types
    for name, value in (("fullname", fullname), ("biography", biography),
                        ("current_status", current_status)):
        if not isinstance(value, str):
            raise TypeError(f"Argument '{name}' must be a string, got {type(value).__name__}")

    # Escape user-provided content to prevent XSS
    escaped_fullname = html.escape(fullname, quote=True)
    escaped_biography = html.escape(biography, quote=True)
    escaped_status = html.escape(current_status, quote=True)

    # Populate the template safely
    formatted_profile: str = PROFILE_FORMAT.format(
        fullname=escaped_fullname,
        biography=escaped_biography,
        current_status=escaped_status
    )

    return formatted_profile