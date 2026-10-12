import xml.sax.saxutils

# Predefined XML template with a placeholder for user input.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_input}</content>
</response>"""

def create_xml_output(user_input: str) -> str:
    """
    Safely embed user-provided content into an XML template.

    Parameters
    ----------
    user_input : str
        The string provided by the user to be included in the XML.

    Returns
    -------
    str
        A well‑formed XML document containing the escaped user input.
    """
    # Escape special XML characters to prevent injection or malformed XML.
    safe_input = xml.sax.saxutils.escape(user_input, {"'": "&apos;", '"': "&quot;"})
    return xml_template.format(user_input=safe_input)