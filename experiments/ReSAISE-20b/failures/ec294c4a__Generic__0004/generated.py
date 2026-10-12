# build_event_invitation.py

import html
from typing import Any


# Pre‑defined HTML template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} – Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .invitation {{ border: 1px solid #ccc; padding: 2rem; border-radius: 8px; }}
        .event-title {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .event-date {{ color: #555; margin-bottom: 1rem; }}
        .event-description {{ white-space: pre-wrap; margin-bottom: 1rem; }}
        .additional-notes {{ font-style: italic; color: #333; }}
    </style>
</head>
<body>
    <div class="invitation">
        <h1 class="event-title">{event_title}</h1>
        <div class="event-date"><strong>Date:</strong> {event_date}</div>
        <p class="event-description">{event_description}</p>
        <p class="additional-notes">{additional_notes}</p>
    </div>
</body>
</html>
"""


def _sanitize(value: str) -> str:
    """
    Escape HTML special characters to prevent XSS attacks.
    Preserves line breaks by converting newline characters into <br> tags after escaping.
    """
    escaped = html.escape(value, quote=True)
    return escaped.replace("\n", "<br>")


def build_event_invitation(
    title_of_event: str,
    details_of_event: str,
    when_event_is: str,
    extra_event_info: str,
) -> str:
    """
    Build a secure HTML invitation string.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A detailed description of the event (may contain newlines).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any additional information or instructions.

    Returns
    -------
    str
        A sanitized HTML representation of the invitation.
    """
    if not isinstance(title_of_event, str):
        raise TypeError("title_of_event must be a string")
    if not isinstance(details_of_event, str):
        raise TypeError("details_of_event must be a string")
    if not isinstance(when_event_is, str):
        raise TypeError("when_event_is must be a string")
    if not isinstance(extra_event_info, str):
        raise TypeError("extra_event_info must be a string")

    sanitized_title = _sanitize(title_of_event)
    sanitized_description = _sanitize(details_of_event)
    sanitized_date = _sanitize(when_event_is)
    sanitized_notes = _sanitize(extra_event_info)

    return INVITATION_FORMAT.format(
        event_title=sanitized_title,
        event_description=sanitized_description,
        event_date=sanitized_date,
        additional_notes=sanitized_notes,
    )