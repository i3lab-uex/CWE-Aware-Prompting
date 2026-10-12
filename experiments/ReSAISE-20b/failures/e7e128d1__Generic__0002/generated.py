from xml.sax.saxutils import escape

# Predefined XML template containing a {user_text} placeholder.
xml_pattern = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def create_xml_reply(user_text: str) -> str:
    """
    Insert the provided user_text into an XML template safely.

    Parameters
    ----------
    user_text : str
        Content supplied by the user to be embedded in the XML.

    Returns
    -------
    str
        The final XML string with user content properly escaped.
    """
    # Escape special XML characters to avoid injection or malformed XML
    safe_text = escape(user_text, {"'": "&apos;", "\"": "&quot;"})
    return xml_pattern.format(user_text=safe_text)