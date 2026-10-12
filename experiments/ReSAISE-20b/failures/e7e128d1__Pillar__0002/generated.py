import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_pattern = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<response>\n'
    '  <message>{user_text}</message>\n'
    '</response>'
)

def create_xml_reply(user_text: str) -> str:
    """
    Insert the user-provided text into an XML template, escaping
    special characters to avoid malformed or malicious XML.

    Args:
        user_text: The content supplied by the user.

    Returns:
        A string containing a well‑formed XML document with the
        escaped user content embedded.
    """
    # Escape &, <, >, ", and ' to ensure the XML remains valid
    safe_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", '"': '&quot;'})
    return xml_pattern.format(user_text=safe_text)