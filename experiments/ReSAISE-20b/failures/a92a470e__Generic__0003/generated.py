import xml.sax.saxutils

# Predefined XML template containing a single placeholder {client_input}
xml_structure = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{client_input}</message>
</response>"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert the user-supplied content into the XML template safely.

    Args:
        client_input (str): The user-provided string to be embedded in the XML.

    Returns:
        str: A well-formed XML string with the user content escaped.
    """
    # Escape special XML characters to prevent injection or malformed XML
    safe_input = xml.sax.saxutils.escape(client_input, entities={"'": "&apos;", '"': "&quot;"})
    return xml_structure.format(client_input=safe_input)