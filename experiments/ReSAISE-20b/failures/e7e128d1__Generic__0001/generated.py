import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_pattern = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def create_xml_reply(user_text: str) -> str:
    """
    Insert the supplied user text into an XML template, escaping
    any characters that would break the XML structure.

    Parameters:
        user_text (str): The content submitted by the user.

    Returns:
        str: The final XML string with the escaped user text inserted.
    """
    # Escape characters that have special meaning in XML
    safe_text = xml.sax.saxutils.escape(user_text)
    return xml_pattern.format(user_text=safe_text)