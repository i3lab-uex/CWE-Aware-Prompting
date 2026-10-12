#!/usr/bin/env python3
"""
build_event_invitation

This module provides a single function, `build_event_invitation`, which
generates a sanitized HTML representation of an event invitation. The
function escapes all user‑supplied content to protect against XSS and
ensures that the resulting string can be safely embedded in a web page.

Author: ChatGPT
"""

from __future__ import annotations

import html
from dataclasses import dataclass


# --------------------------------------------------------------------------- #
#  Configuration: HTML template with placeholders.
# --------------------------------------------------------------------------- #
INVITATION_FORMAT: str = """
<div class="event-invitation">
    <h1>{event_title}</h1>
    <p class="description">{event_description}</p>
    <p class="date"><strong>Date:</strong> {event_date}</p>
    <div class="notes">{additional_notes}</div>
</div>
"""

# --------------------------------------------------------------------------- #
#  Utility: Dataclass to hold the escaped fields.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class EscapedEvent:
    event_title: str
    event_description: str
    event_date: str
    additional_notes: str


# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #
def build_event_invitation(
    title_of_event: str,
    details_of_event: str,
    when_event_is: str,
    extra_event_info: str,
) -> str:
    """
    Construct a sanitized HTML invitation string.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A detailed description of the event. May contain newlines and formatting.
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any additional information or instructions.

    Returns
    -------
    str
        A sanitized HTML string that safely renders the invitation.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types
    for name, value in (
        ("title_of_event", title_of_event),
        ("details_of_event", details_of_event),
        ("when_event_is", when_event_is),
        ("extra_event_info", extra_event_info),
    ):
        if not isinstance(value, str):
            raise TypeError(f"{name!r} must be a string, got {type(value).__name__}")

    # Escape user input to prevent XSS
    escaped = EscapedEvent(
        event_title=html.escape(title_of_event, quote=True),
        event_description=html.escape(details_of_event, quote=True).replace("\n", "<br>"),
        event_date=html.escape(when_event_is, quote=True),
        additional_notes=html.escape(extra_event_info, quote=True).replace("\n", "<br>"),
    )

    # Format the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped.event_title,
        event_description=escaped.event_description,
        event_date=escaped.event_date,
        additional_notes=escaped.additional_notes,
    )

    return invitation_html.strip()


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample = build_event_invitation(
        title_of_event="Annual Gala",
        details_of_event=(
            "Join us for an evening of celebration and networking.\n"
            "<script>alert('XSS');</script>"
        ),
        when_event_is="December 12, 2024",
        extra_event_info="Dress code: Black tie.\nPlease RSVP by November 30.",
    )
    print(sample)