import xml.sax.saxutils

# The XML template with a placeholder for user-provided content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_input}</message>
</response>"""

def create_xml_output(user_input: str) -> str:
    """
    Safely embed user input into an XML template by escaping special characters.

    Parameters
    ----------
    user_input : str
        Input provided by the user that will be inserted into the XML structure.

    Returns
    -------
    str
        A fully-formed XML string with the user content safely escaped.
    """
    # Escape &, <, >, " and ' to prevent XML injection (CWE-74)
    safe_input = xml.sax.saxutils.escape(user_input, {"'": "&apos;", '"': "&quot;"})
    return xml_template.format(user_input=safe_input)