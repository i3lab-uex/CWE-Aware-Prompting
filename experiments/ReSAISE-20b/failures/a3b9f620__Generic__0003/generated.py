# -*- coding: utf-8 -*-
"""
Utility to generate a sanitized user profile string for web display.
"""

from html import escape

# Example template. In real usage, this would be defined elsewhere
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{full_name}</h1>\n"
    "  <p class='about'>{about_me}</p>\n"
    "  <footer>{status_update}</footer>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML representation of a user's profile.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted profile string ready for web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    ValueError
        If the resulting formatted profile would be empty or too large.
    """
    # Validate argument types
    for arg_name, value in (
        ("full_name", full_name),
        ("about_me", about_me),
        ("status_update", status_update),
    ):
        if not isinstance(value, str):
            raise TypeError(f"{arg_name} must be a string, got {type(value).__name__}")

    # Sanitize user input to prevent XSS
    safe_name = escape(full_name, quote=True)
    safe_about = escape(about_me, quote=False)  # preserve line breaks as <br> if needed
    safe_status = escape(status_update, quote=True)

    # Build the profile using the predefined format
    profile_html = PROFILE_FORMAT.format(
        full_name=safe_name,
        about_me=safe_about,
        status_update=safe_status,
    )

    # Basic sanity check: ensure the output is not empty and within reasonable size
    if not profile_html.strip():
        raise ValueError("Generated profile is empty.")
    if len(profile_html) > 10_000:  # arbitrary limit to prevent abuse
        raise ValueError("Generated profile is too large.")

    return profile_html