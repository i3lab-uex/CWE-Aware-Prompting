import html

# Predefined HTML template with placeholders for the invitation components.
INVITATION_FORMAT = """
<div class="event-invitation" style="font-family:Arial,Helvetica,sans-serif; border:1px solid #ccc; padding:15px; max-width:600px;">
    <h2>{title_of_event}</h2>
    <p style="white-space:pre-wrap;">{event_details}</p>
    <p><strong>When:</strong> {scheduled_date}</p>
    <div style="margin-top:10px;">
        {extra_info}
    </div>
</div>
"""

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generates a sanitized HTML string for an event invitation.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event (may contain newlines).
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A sanitized HTML string ready for safe rendering in a browser.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (title_of_event, event_details, scheduled_date, extra_info)):
        raise TypeError("All arguments must be of type str")

    # Escape all user-provided content to prevent XSS
    escaped_title = html.escape(title_of_event, quote=True)
    escaped_details = html.escape(event_details, quote=True)
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_extra = html.escape(extra_info, quote=True)

    # Render the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        title_of_event=escaped_title,
        event_details=escaped_details,
        scheduled_date=escaped_date,
        extra_info=escaped_extra
    )

    return invitation_html.strip()