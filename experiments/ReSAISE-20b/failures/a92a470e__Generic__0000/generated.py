import xml.sax.saxutils

# Predefined XML template with a placeholder for client input.
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert the supplied client input into the XML template, ensuring that
    any characters that could break the XML structure are properly escaped.

    Parameters:
        client_input (str): The raw content provided by the user.

    Returns:
        str: A well‑formed XML string containing the escaped client input.
    """
    # Escape special XML characters to prevent injection or malformed XML.
    safe_input = xml.sax.saxutils.escape(client_input, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped input.
    return xml_structure.format(client_input=safe_input)