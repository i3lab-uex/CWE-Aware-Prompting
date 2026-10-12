import xml.sax.saxutils

# Predefined XML template with a placeholder for user text.
xml_pattern = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def create_xml_reply(user_text: str) -> str:
    """
    Create an XML reply by safely inserting user-supplied text into a template.

    Parameters
    ----------
    user_text : str
        The content submitted by the user that will be placed into the XML template.

    Returns
    -------
    str
        The final XML response with user content included at the appropriate position
        in the template. Special characters are escaped to prevent XML injection.

    Notes
    -----
    This function uses ``xml.sax.saxutils.escape`` to neutralize characters that have
    special meaning in XML (e.g., <, >, &, ', "). This mitigates CWE-74 by ensuring
    that the inserted content cannot break out of the intended XML structure.
    """
    # Escape special XML characters to avoid injection
    safe_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_pattern.format(user_text=safe_text)