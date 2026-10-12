#!/usr/bin/env python3
"""
User profile rendering module.

This module defines a single public function `display_user_profile` that
takes user supplied data and returns an HTML snippet ready for safe display.
The function performs basic sanitisation (HTML escaping) and enforces
reasonable length limits to mitigate potential security issues such as
CWE-707 (improper neutralisation of structured messages).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import html
import textwrap
from typing import Final

# --------------------------------------------------------------------------- #
# Configuration: template for the user profile display.
#
# The placeholders are named `{name}`, `{bio}` and `{status}`.
PROFILE_FORMAT: Final[str] = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <div class="status">{status}</div>
</div>
"""

# --------------------------------------------------------------------------- #
# Constants for input validation
MAX_NAME_LENGTH: Final[int] = 50
MAX_BIO_LENGTH: Final[int] = 1000
MAX_STATUS_LENGTH: Final[int] = 200

# --------------------------------------------------------------------------- #
def _truncate(text: str, limit: int) -> str:
    """
    Truncate a string to `limit` characters. If the text is longer, it
    appends an ellipsis.
    """
    if len(text) <= limit:
        return text
    return text[:limit - 3] + "..."

# --------------------------------------------------------------------------- #
def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized HTML snippet representing a user profile.

    Parameters
    ----------
    person_name : str
        The user's self-provided name.
    user_bio : str
        A multi-sentence biography authored by the user.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string with placeholders replaced by sanitized content,
        ready for safe rendering in a web interface.

    Raises
    ------
    ValueError
        If any required argument is missing or if the template does not
        contain all expected placeholders.
    """
    # Basic sanity checks for arguments
    if not isinstance(person_name, str):
        raise ValueError("person_name must be a string")
    if not isinstance(user_bio, str):
        raise ValueError("user_bio must be a string")
    if not isinstance(status_message, str):
        raise ValueError("status_message must be a string")

    # Ensure the template contains all required placeholders
    expected_placeholders = {"{name}", "{bio}", "{status}"}
    template_placeholders = {
        ph for ph in expected_placeholders if ph in PROFILE_FORMAT
    }
    missing = expected_placeholders - template_placeholders
    if missing:
        raise ValueError(f"PROFILE_FORMAT is missing placeholders: {missing}")

    # Truncate inputs to reasonable limits
    person_name = _truncate(person_name.strip(), MAX_NAME_LENGTH)
    user_bio = _truncate(user_bio.strip(), MAX_BIO_LENGTH)
    status_message = _truncate(status_message.strip(), MAX_STATUS_LENGTH)

    # Escape HTML special characters to prevent XSS
    escaped_name = html.escape(person_name, quote=True)
    escaped_bio = html.escape(user_bio, quote=False).replace("\n", "<br>")
    escaped_status = html.escape(status_message, quote=True)

    # Format the final HTML
    rendered_profile = PROFILE_FORMAT.format(
        name=escaped_name,
        bio=escaped_bio,
        status=escaped_status,
    )

    # Optionally, wrap the output in a safety wrapper
    return rendered_profile.strip()

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple test
    example_name = "<script>alert('xss')</script>John Doe"
    example_bio = "I love coding.\nHere is a link: <a href='https://example.com'>Example</a>"
    example_status = "Working on a new project! 🚀"

    print(display_user_profile(example_name, example_bio, example_status))