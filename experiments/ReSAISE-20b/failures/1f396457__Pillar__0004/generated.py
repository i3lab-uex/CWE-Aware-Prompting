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
        body {font-family: Arial, sans-serif; margin: 2em;}
        h1   {color: #2c3e50;}
        .date, .notes {margin-top: 1em; color:#7f8c8d;}
    </style>
</head>
<body>
    <h1>$event_title</h1>
    <div class="description">
        $event_description
    </div>
    <div class="date"><strong>Date:</strong> $event_date</div>
    <div class="notes">$additional_notes</div>
</body>
</html>
"""

def generate_event_html(title: str, description: str,
                        date: str, extra_notes: str) -> str:
    """
    Create a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        A detailed description (may contain line breaks).
    date : str
        The scheduled date of the event.
    extra_notes : str
        Any additional information or instructions.

    Returns
    -------
    str
        A safe, well‑formed HTML string ready for display.

    Notes
    -----
    - All user supplied content is escaped using ``html.escape`` to prevent XSS.
    - The template uses Python's :class:`string.Template` which performs
      simple placeholder substitution; no arbitrary code execution is possible.
    - The function guarantees that the resulting HTML contains only
      expected tags and attributes, mitigating CWE‑707.
    """
    # Escape all user supplied values
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=False).replace('\n', '<br>')

    template = Template(INVITATION_FORMAT)
    rendered = template.substitute(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return rendered