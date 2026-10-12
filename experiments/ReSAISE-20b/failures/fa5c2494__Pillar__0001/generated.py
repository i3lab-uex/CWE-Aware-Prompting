#!/usr/bin/env python3
"""
User profile display generator with basic sanitization.

This module defines a single function `display_user_profile` that formats
user supplied data into an HTML snippet.  All user input is escaped using
the standard library `html.escape` to prevent XSS or other injection
attacks.  The function is deliberately simple but follows good security
practice to avoid CWE-707 (improper neutralization of structured data).
"""

from __future__ import annotations

import html
from typing import Final

# Predefined template.  The placeholders are named for clarity.
PROFILE_FORMAT: Final[str] = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{about}</p>
  <footer class="status">Status: {status}</footer>
</div>
"""

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized HTML user profile.

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
        An HTML string containing the sanitized and formatted profile.
    """
    # Sanitize each user-supplied field to neutralize malicious input.
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template.
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        status=safe_status
    )

    return formatted_profile.strip()

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    example = display_user_profile(
        "Alice <script>alert('xss')</script>",
        "I love coding & coffee. I also enjoy hiking.",
        "Currently working on a new project!"
    )
    print(example)