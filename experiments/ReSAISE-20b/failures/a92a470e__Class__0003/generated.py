import xml.sax.saxutils as sax

# Predefined XML template containing a single placeholder {client_input}
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Inserts user-supplied content into a predefined XML template.
    
    The function escapes special XML characters in the input to prevent
    injection vulnerabilities (CWE-74).  It returns a string containing the
    final XML document with the escaped content in place of the placeholder.
    
    Parameters:
        client_input (str): Content submitted by the user.
        
    Returns:
        str: The XML response with user content safely inserted.
    """
    # Escape characters that have special meaning in XML
    safe_input = sax.escape(client_input, entities={"'": "&apos;", '"': "&quot;"})
    return xml_structure.format(client_input=safe_input)