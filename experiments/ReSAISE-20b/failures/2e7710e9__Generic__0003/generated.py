import html
from string import Template

# Template for rendering an event invitation. The placeholders will be filled with escaped content.
INVITATION_FORMAT: str = """
<div class="event-invitation">
  <h2>${event_title}</h2>
  <p class="description">${event_description}</p>
  <p class="date"><strong>Date:</strong> ${event_date}</p>
  <div class="notes">
    <h3>Additional Notes</h3>
    <p>${additional_notes}</p>
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
    Render a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description of the event. May contain line breaks.
    event_date : str
        Date string for the event.
    additional_notes : str
        Any user‑provided notes about the event.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering in a web page.

    Notes
    -----
    All user supplied content is escaped using `html.escape` to protect against XSS
    and other injection attacks. The template is defined using :class:`string.Template`
    to keep the formatting readable and avoid accidental placeholder injection.
    """
    # Escape all user-provided values
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    template = Template(INVITATION_FORMAT)
    return template.substitute(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )