import xml.sax.saxutils as saxutils

# Predefined XML template with a placeholder for user input
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_input}</message>
</response>"""

def create_xml_output(user_input: str) -> str:
    """
    Embed the provided user input into a predefined XML template safely.

    Args:
        user_input (str): The raw string supplied by the user that must be
                          inserted into the XML response.

    Returns:
        str: A fully-formed XML string with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection or malformed XML
    safe_input = saxutils.escape(user_input, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return xml_template.format(user_input=safe_input)