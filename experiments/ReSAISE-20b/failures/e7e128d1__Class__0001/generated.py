import xml.sax.saxutils

# Predefined XML template with a placeholder for user-supplied text
xml_pattern = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def create_xml_reply(user_text: str) -> str:
    """
    Construct an XML response by inserting the supplied user text into a
    predefined XML template. The function safely escapes special XML
    characters to prevent injection vulnerabilities (CWE-74).

    Args:
        user_text: The text supplied by the user.

    Returns:
        A string containing the complete XML response.
    """
    # Escape special XML characters in the user-supplied text
    safe_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped text
    return xml_pattern.format(user_text=safe_text)