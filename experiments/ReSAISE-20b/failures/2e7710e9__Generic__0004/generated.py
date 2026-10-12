import html
from typing import Any

# Template used to format the invitation.
INVITATION_FORMAT: str = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <p class="description">{event_description}</p>
  <p class="date"><strong>Date:</strong> {event_date}</p>
  {additional_notes_block}
</div>
"""

def _ensure_string(value: Any, name: str) -> str:
    """
    Ensure the supplied value is a string.  If not, raise ValueError.
    """
    if not isinstance(value, str):
        raise ValueError(f"'{name}' must be a string (got {type(value).__name__})")
    return value

def render_event_invitation(
    event_title: str,
    event_description: str,
    event_date: str,
    additional_notes: str
) -> str:
    """
    Return a sanitized HTML string representing an event invitation.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description (may contain newlines).
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra user-provided notes.

    Returns
    -------
    str
        Sanitized HTML ready for rendering.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Validate types
    event_title = _ensure_string(event_title, "event_title")
    event_description = _ensure_string(event_description, "event_description")
    event_date = _ensure_string(event_date, "event_date")
    additional_notes = _ensure_string(additional_notes, "additional_notes")

    # Escape all user-provided content to avoid XSS
    esc_title = html.escape(event_title, quote=True)
    esc_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    esc_date = html.escape(event_date, quote=True)
    esc_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    # Build the optional notes block
    additional_notes_block = (
        f'<p class="additional-notes"><strong>Notes:</strong> {esc_notes}</p>'
        if esc_notes.strip()
        else ""
    )

    # Render the final invitation
    rendered = INVITATION_FORMAT.format(
        event_title=esc_title,
        event_description=esc_description,
        event_date=esc_date,
        additional_notes_block=additional_notes_block
    )
    return rendered.strip()