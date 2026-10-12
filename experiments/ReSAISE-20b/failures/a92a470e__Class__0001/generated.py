import xml.sax.saxutils

# Predefined XML template with a placeholder for the client input.
xml_structure = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{client_input}</message>
</response>"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert user-supplied content into an XML template safely.

    Parameters
    ----------
    client_input : str
        The raw content supplied by the user. It will be escaped to prevent
        XML injection attacks.

    Returns
    -------
    str
        The final XML document with the escaped user content inserted in
        place of the placeholder.
    """
    # Escape special XML characters to avoid injection or malformed XML
    safe_input = xml.sax.saxutils.escape(client_input, {"\"": "&quot;", "'": "&#39;"})
    return xml_structure.format(client_input=safe_input)