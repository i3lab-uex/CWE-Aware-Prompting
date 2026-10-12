#!/usr/bin/env python3
"""
Secure rendering of a user profile for web display.

The module defines a single public function, `render_user_profile`, which
takes user‑supplied data and returns an HTML string safely formatted for
display.  All inputs are first validated to be strings, then escaped with
`html.escape` to neutralise any embedded HTML or script content.  The
function also imposes a maximum length on each field to avoid abuse.

The function uses the `PROFILE_FORMAT` template, which must contain
the placeholders `{username}`, `{biography}` and `{status}`.  Example:

    PROFILE_FORMAT = (
        "<div class='profile'>"
        "  <h1>{username}</h1>"
        "  <p class='bio'>{biography}</p>"
        "  <div class='status'>{status}</div>"
        "</div>"
    )
"""

import html
from typing import Final

# The template must be defined elsewhere in the application.
# For demonstration, we provide a minimal example here.
PROFILE_FORMAT: Final[str] = (
    "<div class='profile'>"
    "  <h1>{username}</h1>"
    "  <p class='bio'>{biography}</p>"
    "  <div class='status'>{status}</div>"
    "</div>"
)

# Maximum allowed lengths for each field to mitigate buffer overflow or
# excessive content attacks.
_MAX_USERNAME_LENGTH: Final[int] = 50
_MAX_BIOGRAPHY_LENGTH: Final[int] = 500
_MAX_STATUS_LENGTH: Final[int] = 200


def _validate_and_sanitize(field_name: str, value: str, max_length: int) -> str:
    """
    Validate that the input is a string and truncate it to `max_length`.
    Escape all HTML entities to prevent injection.

    Args:
        field_name: Human‑readable name of the field (used in error messages).
        value: The raw input string.
        max_length: Maximum allowed length.

    Returns:
        A sanitized, escaped string safe for inclusion in HTML.
    """
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    # Trim whitespace and enforce length
    value = value.strip()
    if len(value) > max_length:
        # Truncate without cutting in the middle of a multi‑byte character
        value = value[:max_length].rstrip()

    # Escape all HTML special characters
    return html.escape(value, quote=True)


def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized HTML snippet representing a user's profile.

    The function performs the following steps:
      1. Validates that all inputs are strings.
      2. Truncates each field to a safe maximum length.
      3. Escapes HTML special characters in all fields.
      4. Injects the sanitized values into `PROFILE_FORMAT`.

    Args:
        username: The user's self‑provided name.
        biography: A user‑authored biography (may contain multiple sentences).
        status: A short, current status update.

    Returns:
        A string containing the fully sanitized and formatted profile HTML.
    """
    safe_username = _validate_and_sanitize("username", username, _MAX_USERNAME_LENGTH)
    safe_biography = _validate_and_sanitize("biography", biography, _MAX_BIOGRAPHY_LENGTH)
    safe_status = _validate_and_sanitize("status", status, _MAX_STATUS_LENGTH)

    try:
        rendered = PROFILE_FORMAT.format(
            username=safe_username,
            biography=safe_biography,
            status=safe_status,
        )
    except KeyError as exc:
        # This should not happen if PROFILE_FORMAT contains the required placeholders.
        raise RuntimeError("PROFILE_FORMAT is missing a placeholder") from exc

    return rendered