import xml.sax.saxutils as saxutils

# Pre‑defined XML template with a placeholder for user content.
xml_template = """
<message>
    <header>
        <timestamp>{timestamp}</timestamp>
    </header>
    <body>
        {content_insert}
    </body>
</message>
"""

def generate_xml_message(content_insert: str) -> str:
    """
    Safely inserts user supplied content into an XML template.

    Parameters
    ----------
    content_insert : str
        The user supplied text that will be inserted into the <body> element.

    Returns
    -------
    str
        The fully constructed XML string with special characters escaped.
    """
    # Escape any XML-sensitive characters to prevent injection attacks
    safe_content = saxutils.escape(content_insert)

    # Optionally, add a timestamp or other context data
    from datetime import datetime
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Format the template with the escaped content and timestamp
    return xml_template.format(
        timestamp=timestamp,
        content_insert=safe_content
    )