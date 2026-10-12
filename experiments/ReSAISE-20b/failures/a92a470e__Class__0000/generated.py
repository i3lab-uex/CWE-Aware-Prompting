import xml.sax.saxutils as saxutils

# Predefined XML template containing a placeholder for user input
xml_structure = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{client_input}</message>
</response>"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert user-supplied content into a predefined XML template.

    Args:
        client_input (str): Content provided by the user.

    Returns:
        str: The XML response with the escaped user content inserted.
    """
    # Escape special characters to prevent XML injection (CWE‑74)
    safe_input = saxutils.escape(client_input, entities={"'": "&apos;", '"': "&quot;"})
    return xml_structure.format(client_input=safe_input)