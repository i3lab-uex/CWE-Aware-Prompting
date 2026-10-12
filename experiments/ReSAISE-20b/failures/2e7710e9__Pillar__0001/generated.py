# -*- coding: utf-8 -*-

"""
Utility for rendering a safe HTML event invitation.

The function `render_event_invitation` takes raw user input, escapes it to
prevent cross‑site scripting (XSS) attacks, and injects the escaped values
into a predefined invitation template.  The output is a fully‑formed,
well‑structured HTML string suitable for rendering in a browser.

CWE-707 (Improper Neutralization of Structured Data) is mitigated by
strictly escaping all user‑supplied content before it can be interpreted
as HTML or JavaScript.  No untrusted data is passed to `format` without
escaping.
"""

from __future__ import annotations

import html
from typing import Final


# Template for the invitation.  The placeholders are intentionally simple
# and will be replaced by escaped values.
INVITATION_FORMAT: Final[str] = """
<div class="invitation">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="description">
        {event_description}
    </div>
    <div class="notes">
        <h2>Additional Notes</h2>
        {additional_notes}
    </div>
</div>
"""


def render_event_invitation(
    event_title: str,
    event_description: str,
    event_date: str,
    additional_notes: str
) -> str:
    """
    Render a sanitized HTML invitation.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description (may contain line breaks).
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra notes from the user.

    Returns
    -------
    str
        A safe, well‑formed HTML string ready for rendering.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """

    # Validate input types early
    if not all(isinstance(arg, str) for arg in (
        event_title,
        event_description,
        event_date,
        additional_notes
    )):
        raise TypeError("All arguments must be of type str")

    # Escape all user inputs to neutralize any embedded markup or scripts.
    escaped_title = html.escape(event_title, quote=True)
    escaped_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(event_date, quote=True)
    escaped_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    # Format the invitation using the sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )

    return invitation_html.strip()