#!/usr/bin/env python3
"""
build_event_invitation.py

Creates a secure, sanitized HTML invitation from user supplied data.
"""

import html
from string import Template

# Pre‑defined HTML template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>$event_title</title>
    <style>
        body {font-family: Arial, sans-serif; line-height: 1.6;}
        .event-title {font-size: 2em; margin-bottom: 0.5em;}
        .event-date {font-size: 1.2em; color: #555;}
        .event-description, .additional-notes {margin-top: 1em;}
    </style>
</head>
<body>
    <div class="event">
        <h1 class="event-title">$event_title</h1>
        <p class="event-date"><strong>Date:</strong> $event_date</p>
        <div class="event-description">
            <h2>Description</h2>
            <p>$event_description</p>
        </div>
        $additional_notes_block
    </div>
</body>
</html>
"""

def build_event_invitation(
        title_of_event: str,
        details_of_event: str,
        when_event_is: str,
        extra_event_info: str
) -> str:
    """
    Produce a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    title_of_event : str
        The heading of the event.
    details_of_event : str
        A detailed description (may contain newlines or user‑generated content).
    when_event_is : str
        The scheduled date of the event.
    extra_event_info : str
        Any supplementary notes or instructions.

    Returns
    -------
    str
        A fully sanitized HTML string ready for rendering in a browser.

    Raises
    ------
    ValueError
        If any required argument is missing or not a string.
    """

    # Validate inputs are strings
    for name, value in [
        ("title_of_event", title_of_event),
        ("details_of_event", details_of_event),
        ("when_event_is", when_event_is),
        ("extra_event_info", extra_event_info)
    ]:
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")

    # Escape user supplied content to neutralise XSS vectors
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=False).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=False).replace("\n", "<br>")

    # Prepare the additional notes block only if there is content
    if safe_notes.strip():
        notes_block = f"""
        <div class="additional-notes">
            <h2>Additional Notes</h2>
            <p>{safe_notes}</p>
        </div>
        """
    else:
        notes_block = ""

    # Create a Template instance and substitute placeholders
    tmpl = Template(INVITATION_FORMAT)
    sanitized_html = tmpl.substitute(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_block=notes_block
    )

    return sanitized_html

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(build_event_invitation(
        title_of_event="Annual Gala & Celebration",
        details_of_event="Join us for an evening of fun, food, and festivities.\nDon't miss the live DJ!",
        when_event_is="2026-12-31",
        extra_event_info="Dress code: Formal attire.\nParking available on site."
    ))