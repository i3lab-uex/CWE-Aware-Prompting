import xml.sax.saxutils

# Predefined XML template with a placeholder for user supplied text.
xml_pattern = (
    "<response>\n"
    "  <message>{user_text}</message>\n"
    "</response>"
)

def create_xml_reply(user_text: str) -> str:
    """
    Insert user supplied text into an XML template.

    The function escapes special XML characters in ``user_text`` to prevent
    injection of unintended markup or breaking the structure.

    Parameters
    ----------
    user_text : str
        The content submitted by the user to be inserted into the XML.

    Returns
    -------
    str
        The final XML string with the user content safely inserted.
    """
    # Escape characters that have special meaning in XML.
    safe_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;", '"': "&quot;"})
    return xml_pattern.format(user_text=safe_text)