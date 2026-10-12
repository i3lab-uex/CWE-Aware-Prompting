import html

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting the user supplied content into a predefined
    template.  The function escapes special XML characters in the input to avoid
    malformed output or injection attacks.

    Parameters:
        input_content (str): The user supplied text to embed in the XML structure.

    Returns:
        str: The final XML string with the escaped input content inserted.
    """
    # Predefined XML template with a placeholder for user content
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_content}</message>
</response>"""

    # Escape the input content for XML
    escaped_content = html.escape(input_content, quote=True)

    # Insert the escaped content into the template
    return xml_template.format(input_content=escaped_content)