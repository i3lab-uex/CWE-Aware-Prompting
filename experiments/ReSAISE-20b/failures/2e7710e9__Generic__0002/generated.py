import html
from string import Template

# Template for the invitation. Placeholders are ${event_title}, etc.
INVITATION_FORMAT: str = """
<div class="invitation">
    <h2>${event_title}</h2>
    <p><strong>Date:</strong> ${event_date}</p>
    <div class="description">${event_description}</div>
    <footer>${additional_notes}</footer>
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
        Full description (may contain multiple lines).
    event_date : str
        Date of the event.
    additional_notes : str
        User-provided extra notes.

    Returns
    -------
    str
        Sanitized HTML content ready for rendering.
    """
    # Escape all user-provided fields to prevent XSS
    safe_title = html.escape(event_title, quote=True)
    # Preserve line breaks in description by converting \n to <br>
    safe_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True)

    # Use Template to safely substitute the placeholders
    template = Template(INVITATION_FORMAT)
    rendered_html = template.substitute(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return rendered_html.strip()