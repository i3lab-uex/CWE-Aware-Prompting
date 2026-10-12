import xml.sax.saxutils as sax

# Predefined XML structure containing a placeholder for user input.
xml_structure = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{client_input}</message>
</response>"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert user-provided content into an XML template safely.

    Parameters
    ----------
    client_input : str
        The raw content supplied by the user.

    Returns
    -------
    str
        A well‑formed XML string with the escaped user content.
    """
    # Escape special XML characters to prevent injection or malformed XML
    safe_input = sax.escape(client_input, {"'": "&apos;", '"': "&quot;"})
    return xml_structure.format(client_input=safe_input)