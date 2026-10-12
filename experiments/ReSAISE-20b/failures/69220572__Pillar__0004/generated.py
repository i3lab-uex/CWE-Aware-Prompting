# SPDX-License-Identifier: MIT

"""
Secure event invitation generator.

This module provides a single function `create_event_invitation` that
creates an HTML representation of an event invitation while properly
escaping user-supplied content to prevent XSS and other injection attacks.
"""

import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_of_event}</title>
</head>
<body>
    <h1>{title_of_event}</h1>
    <div>{event_details}</div>
    <p><strong>Scheduled Date:</strong> {scheduled_date}</p>
    <div>{extra_info}</div>
</body>
</html>
"""

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event (may contain multiple lines).
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.

    Notes
    -----
    All user-supplied fields are escaped using `html.escape` to neutralize any
    embedded HTML or JavaScript, mitigating XSS attacks (CWE-79) and ensuring
    that the output remains well‑formed HTML (CWE-707).
    """
    # Escape all user inputs
    safe_title = html.escape(title_of_event, quote=True)
    safe_details = html.escape(event_details, quote=True).replace("\n", "<br>")
    safe_date = html.escape(scheduled_date, quote=True)
    safe_extra = html.escape(extra_info, quote=True).replace("\n", "<br>")

    # Format the invitation using the template
    return INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )