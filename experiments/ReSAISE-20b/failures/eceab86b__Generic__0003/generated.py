import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_name} - Invitation</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 2rem; }}
  .invitation {{ border: 1px solid #ccc; padding: 1rem; border-radius: 8px; }}
  h1 {{ color: #2c3e50; }}
  .date {{ font-weight: bold; margin-top: 1rem; }}
  .notes {{ margin-top: 1.5rem; color: #555; }}
</style>
</head>
<body>
<div class="invitation">
  <h1>{event_name}</h1>
  <div class="description">{description_of_event}</div>
  <div class="date">Date: {date_of_event}</div>
  <div class="notes">{notes_for_event}</div>
</div>
</body>
</html>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event (may contain multiple lines).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing safe HTML for displaying the event invitation.

    Raises
    ------
    ValueError
        If any of the required arguments are empty or not a string.
    """
    # Basic validation
    for name, value in {
        "event_name": event_name,
        "description_of_event": description_of_event,
        "date_of_event": date_of_event,
        "notes_for_event": notes_for_event
    }.items():
        if not isinstance(value, str):
            raise ValueError(f"'{name}' must be a string.")
        if not value.strip():
            raise ValueError(f"'{name}' cannot be empty or whitespace only.")

    # Escape user-supplied content to prevent XSS attacks
    safe_event_name = html.escape(event_name)
    safe_description = html.escape(description_of_event).replace("\n", "<br>")
    safe_date = html.escape(date_of_event)
    safe_notes = html.escape(notes_for_event).replace("\n", "<br>")

    # Format the invitation using the predefined template
    return INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )