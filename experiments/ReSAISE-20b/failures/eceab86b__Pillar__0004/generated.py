# -*- coding: utf-8 -*-
"""
Secure event invitation generator.

This module defines a single function `create_invitation_for_event` that
takes event details and returns a sanitized HTML snippet suitable for
displaying on a web page.  All user supplied content is escaped using
`html.escape` to mitigate XSS attacks and other injection vectors.
"""

from __future__ import annotations

import html
from typing import Any, Dict


# --------------------------------------------------------------------------- #
# 1. Define the HTML template with placeholders
# --------------------------------------------------------------------------- #

INVITATION_FORMAT: str = """
<div class="event-invitation">
  <h1>{event_name}</h1>
  <div class="description">{description_of_event}</div>
  <p><strong>Date:</strong> {date_of_event}</p>
  <div class="notes">{notes_for_event}</div>
</div>
"""


# --------------------------------------------------------------------------- #
# 2. Helper: Safe dictionary for formatting
# --------------------------------------------------------------------------- #

class _SafeDict(dict):
    """
    A dict subclass that returns an empty string for missing keys.
    This prevents KeyError during format if a placeholder is omitted.
    """
    def __missing__(self, key: str) -> str:
        return ""


# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive, possibly multi‑line description.  It may contain
        user supplied markup that must be escaped.
    date_of_event : str
        The scheduled date for the event.  It is treated as plain text.
    notes_for_event : str
        Extra information or instructions.  Escaped for safety.

    Returns
    -------
    str
        A string containing sanitized HTML ready for safe rendering.
    """
    # Validate argument types to guard against accidental misuse
    if not all(isinstance(arg, str) for arg in (
        event_name,
        description_of_event,
        date_of_event,
        notes_for_event
    )):
        raise TypeError("All arguments must be strings")

    # Escape all user supplied content
    safe_content: Dict[str, str] = {
        "event_name": html.escape(event_name, quote=True),
        "description_of_event": html.escape(description_of_event, quote=True).replace("\n", "<br>"),
        "date_of_event": html.escape(date_of_event, quote=True),
        "notes_for_event": html.escape(notes_for_event, quote=True).replace("\n", "<br>"),
    }

    # Use a safe dictionary to avoid KeyError if template changes
    formatted = INVITATION_FORMAT.format_map(_SafeDict(safe_content))

    return formatted.strip()


# --------------------------------------------------------------------------- #
# 4. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    example = create_invitation_for_event(
        event_name="Annual Gala",
        description_of_event="Join us for a night of celebration & fun.\n\nDress code: Formal.",
        date_of_event="December 12, 2024",
        notes_for_event="Please RSVP by November 30.\nContact: <script>alert('xss')</script>"
    )
    print(example)