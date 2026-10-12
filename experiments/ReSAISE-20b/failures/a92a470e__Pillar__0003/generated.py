import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Inserts user-supplied content into a predefined XML template,
    escaping any characters that could break the XML structure.

    Parameters
    ----------
    client_input : str
        The content submitted by the user to be embedded in the XML.

    Returns
    -------
    str
        A well‑formed XML string containing the escaped user content.
    """
    # Escape special XML characters to prevent malformed output or injection
    safe_input = xml.sax.saxutils.escape(client_input, {"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content
    return xml_structure.format(client_input=safe_input)