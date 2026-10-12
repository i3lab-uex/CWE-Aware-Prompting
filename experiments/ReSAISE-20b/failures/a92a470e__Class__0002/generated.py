import xml.sax.saxutils

# Predefined XML template containing a placeholder for user content.
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Safely insert user-supplied content into an XML template.

    Parameters
    ----------
    client_input : str
        The raw text submitted by the user that will be inserted into the XML.

    Returns
    -------
    str
        The final XML string with the user content escaped to avoid XML injection.
    """
    # Escape special characters in the user input to prevent XML injection (CWE-74).
    safe_input = xml.sax.saxutils.escape(client_input, entities={
        "'": "&apos;",
        "\"": "&quot;"
    })

    # Format the template with the escaped input.
    return xml_structure.format(client_input=safe_input)