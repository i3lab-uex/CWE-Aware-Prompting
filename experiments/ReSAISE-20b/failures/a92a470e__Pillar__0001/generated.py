import xml.sax.saxutils

# Predefined XML template containing a placeholder for user content.
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert user-supplied content into an XML template, ensuring that the
    inserted text is properly escaped to avoid malformed XML and injection
    vulnerabilities.

    Parameters:
        client_input (str): The raw user content to embed in the XML.

    Returns:
        str: A well‑formed XML string with the escaped user content.
    """
    # Escape special XML characters in the client input
    safe_input = xml.sax.saxutils.escape(client_input, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return xml_structure.format(client_input=safe_input)