import re
from xml.sax.saxutils import escape

# Predefined XML template with a placeholder for user content.
xml_structure = """
<response>
    <message>{client_input}</message>
</response>
"""

def craft_xml_reply(client_input: str) -> str:
    """
    Insert the user-supplied content into the XML template.

    Parameters
    ----------
    client_input : str
        The raw text submitted by the user.

    Returns
    -------
    str
        A well‑formed XML string with the user's content safely escaped.
    """
    # Escape special XML characters to prevent injection attacks
    safe_input = escape(client_input, entities={"'": "&apos;", "\"": "&quot;"})

    # Replace the placeholder with the escaped content
    return xml_structure.format(client_input=safe_input)