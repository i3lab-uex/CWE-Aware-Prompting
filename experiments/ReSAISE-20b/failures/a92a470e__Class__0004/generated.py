import xml.sax.saxutils as sax

# Predefined XML template containing the placeholder `{client_input}`
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert the user supplied content into the XML template safely.

    Parameters
    ----------
    client_input : str
        The user supplied string that will be inserted into the XML template.

    Returns
    -------
    str
        The final XML string with the user content escaped.
    """
    # Escape special XML characters to prevent injection (CWE‑74)
    safe_input = sax.escape(client_input, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped input
    return xml_structure.format(client_input=safe_input)