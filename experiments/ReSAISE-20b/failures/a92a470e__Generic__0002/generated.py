import xml.sax.saxutils

# Predefined XML template containing the placeholder `{client_input}`.
xml_structure = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{client_input}</message>
</response>"""

def craft_xml_reply(client_input: str) -> str:
    """
    Return an XML string where `client_input` is safely inserted into the
    predefined template. Special XML characters in the user input are escaped
    to prevent injection or malformed XML.

    Parameters:
        client_input (str): User supplied content to be embedded in the XML.

    Returns:
        str: The final XML document with user content inserted.
    """
    # Escape special XML characters in the input
    safe_input = xml.sax.saxutils.escape(client_input, {"'": "&apos;", '"': "&quot;"})
    # Insert the escaped input into the template
    return xml_structure.format(client_input=safe_input)