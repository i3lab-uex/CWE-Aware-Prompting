import xml.sax.saxutils

def build_xml_reply(user_text: str) -> str:
    """
    Embed the user supplied text into an XML template safely.

    Parameters
    ----------
    user_text : str
        The content provided by the user that should be inserted into the XML.

    Returns
    -------
    str
        A complete XML string with the user content safely escaped.
    """
    # Predefined template containing a placeholder for user text
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '  <message>{user_text}</message>\n'
        '</response>'
    )

    # Escape special XML characters to prevent injection
    escaped_text = xml.sax.saxutils.escape(user_text, entities={
        "'": "&apos;",  # Optional: escape single quotes if needed
    })

    # Insert the escaped text into the template
    return xml_template.format(user_text=escaped_text)