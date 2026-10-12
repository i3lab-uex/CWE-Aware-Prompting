# -*- coding: utf-8 -*-
"""
Utility module for rendering user profiles safely for web display.
"""

import html
from typing import Any

# Example profile format – in a real application this might come from a config file
PROFILE_FORMAT: str = (
    "<div class=\"profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\"><strong>Status:</strong> {status}</div>\n"
    "</div>"
)


def display_user_profile(
    person_name: str,
    user_bio: str,
    status_message: str
) -> str:
    """
    Construct a safe, sanitized HTML representation of a user profile.

    Parameters
    ----------
    person_name : str
        The user's self-provided name.
    user_bio : str
        A multi-sentence biography authored by the user.
    status_message : str
        A short, current status update.

    Returns
    -------
    str
        An HTML string containing the formatted user profile, with all
        potentially dangerous characters escaped.

    Raises
    ------
    TypeError
        If any argument is not a string.
    ValueError
        If any required argument is empty after stripping whitespace.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise TypeError("All arguments must be of type str")

    # Strip and validate non-empty content
    name_clean = person_name.strip()
    bio_clean = user_bio.strip()
    status_clean = status_message.strip()

    if not name_clean:
        raise ValueError("person_name cannot be empty")
    if not bio_clean:
        raise ValueError("user_bio cannot be empty")
    if not status_clean:
        raise ValueError("status_message cannot be empty")

    # Escape HTML to prevent XSS
    escaped_name = html.escape(name_clean, quote=True)
    escaped_bio = html.escape(bio_clean, quote=True)
    escaped_status = html.escape(status_clean, quote=True)

    # Format the profile using the provided template
    try:
        rendered = PROFILE_FORMAT.format(
            name=escaped_name,
            bio=escaped_bio,
            status=escaped_status
        )
    except KeyError as exc:
        # In case the template has missing placeholders
        raise ValueError(f"Profile format placeholder error: {exc}") from exc

    return rendered