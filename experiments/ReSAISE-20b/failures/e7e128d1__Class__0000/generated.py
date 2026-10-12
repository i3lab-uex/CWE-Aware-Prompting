import xml.sax.saxutils as saxutils

# Predefined XML pattern with a placeholder for user content.
xml_pattern = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def create_xml_reply(user_text: str) -> str:
    """
    Create an XML response by inserting the user-supplied text into a
    predefined template. The function escapes special XML characters to
    mitigate injection vulnerabilities (CWE‑74).

    Parameters:
        user_text (str): Text supplied by the user.

    Returns:
        str: The XML string with the escaped user content inserted.
    """
    # Escape special characters to prevent XML injection
    safe_text = saxutils.escape(user_text, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content
    return xml_pattern.format(user_text=safe_text)