import xml.sax.saxutils as saxutils

# Define the XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_input}</message>
</response>"""

def create_xml_output(user_input: str) -> str:
    """
    Embed the user-provided input into a predefined XML template safely.

    Args:
        user_input (str): The string supplied by the user that must be included
                          in the XML response.

    Returns:
        str: A fully-formed XML string with the user content inserted,
             ensuring that special characters are properly escaped.
    """
    # Escape XML special characters to prevent injection attacks
    safe_input = saxutils.escape(user_input, entities={"'": "&apos;", '"': "&quot;"})
    # Insert the escaped content into the template
    return xml_template.format(user_input=safe_input)