#!/usr/bin/env python3
"""
A secure implementation of a user profile formatter.

The function `display_user_profile` takes raw input from users and
produces an HTML-safe profile string using a predefined template.
It protects against common web injection attacks (CWE‑70, CWE‑707)
by escaping all user-supplied content before interpolation.
"""

import html
from typing import Final

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

# A simple template that will be used to build the final profile.
# The placeholders `{name}`, `{bio}` and `{status}` will be replaced
# with sanitized user input.
PROFILE_FORMAT: Final[str] = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer class=\"status\">{status}</footer>\n"
    "</div>"
)

# Maximum lengths for each field to avoid overly long output
MAX_NAME_LENGTH: Final[int] = 100
MAX_BIO_LENGTH: Final[int] = 2000
MAX_STATUS_LENGTH: Final[int] = 300


# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _truncate(text: str, max_length: int) -> str:
    """Return a string truncated to `max_length` characters."""
    return text[:max_length] if len(text) > max_length else text


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized and formatted user profile string.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi-sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized profile data.

    Raises
    ------
    ValueError
        If any of the arguments is not a string.
    """
    # Type validation
    if not isinstance(username, str):
        raise ValueError("username must be a string")
    if not isinstance(about, str):
        raise ValueError("about must be a string")
    if not isinstance(current_status, str):
        raise ValueError("current_status must be a string")

    # Truncate to avoid excessive output
    username = _truncate(username, MAX_NAME_LENGTH)
    about = _truncate(about, MAX_BIO_LENGTH)
    current_status = _truncate(current_status, MAX_STATUS_LENGTH)

    # Escape all user input to neutralize HTML injection
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=False).replace("\n", "<br>")
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return formatted_profile


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

if __name__ == "__main__":
    sample_profile = display_user_profile(
        username="Jane Doe",
        about=(
            "Software engineer with a passion for open-source projects.\n"
            "Enjoys hiking, cooking, and learning new programming languages."
        ),
        current_status="Currently working on a new web app!"
    )
    print(sample_profile)