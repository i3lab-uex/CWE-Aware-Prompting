import xml.sax.saxutils

# Predefined XML template with a single placeholder for user content.
xml_pattern = """
<response>
    <message>{user_text}</message>
</response>
"""

def create_xml_reply(user_text: str) -> str:
    """
    Insert user supplied text into the XML template safely.

    Parameters
    ----------
    user_text : str
        The content provided by the user to be inserted into the XML.

    Returns
    -------
    str
        The complete XML string with user content escaped and inserted.
    """
    # Escape special XML characters to prevent injection / malformed XML
    safe_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", '"': "&quot;"})
    # Insert the escaped text into the template
    return xml_pattern.format(user_text=safe_text)