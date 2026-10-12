#!/usr/bin/env python3
"""
generate_event_invite.py

Provides a secure HTML representation of an event invitation.
"""

from __future__ import annotations
import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.5; }}
  .invitation {{ border: 2px solid #4CAF50; padding: 20px; max-width: 600px; margin: auto; }}
  .header {{ font-size: 1.5em; margin-bottom: 10px; }}
  .date {{ color: #555; margin-bottom: 15px; }}
  .notes {{ font-style: italic; color: #777; margin-top: 20px; }}
</style>
</head>
<body>
<div class="invitation">
  <div class="header">{title}</div>
  <div class="date">Date: {date}</div>
  <div class="description">{description}</div>
  {notes_block}
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str,
                          date: str, notes: str = "") -> str:
    """
    Generate a sanitized HTML invitation.

    Parameters
    ----------
    title : str
        The event title.
    description : str
        A detailed description (may contain newlines).
    date : str
        The scheduled date for the event.
    notes : str, optional
        Extra information or instructions.

    Returns
    -------
    str
        A complete HTML string ready for safe display.
    """
    # Escape all user-provided content to avoid XSS
    esc_title = html.escape(title, quote=True)
    esc_date = html.escape(date, quote=True)

    # Preserve line breaks in the description by converting newlines to <br>
    esc_description = html.escape(description, quote=True).replace("\n", "<br>")

    if notes:
        esc_notes = html.escape(notes, quote=True).replace("\n", "<br>")
        notes_block = f'<div class="notes">{esc_notes}</div>'
    else:
        notes_block = ""

    return INVITATION_FORMAT.format(
        title=esc_title,
        date=esc_date,
        description=esc_description,
        notes_block=notes_block
    )

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     html_invite = generate_event_invite(
#         title="Annual Gala",
#         description="Join us for an evening of celebration.\nDress code: Formal.",
#         date="2026-12-31",
#         notes="Please RSVP by December 15th."
#     )
#     print(html_invite)