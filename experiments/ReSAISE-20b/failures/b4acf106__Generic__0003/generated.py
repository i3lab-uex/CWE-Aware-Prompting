import xml.sax.saxutils

def generate_xml_response(user_content: str) -> str:
    """
    Generates an XML response by embedding the user-provided content into a template.

    Parameters
    ----------
    user_content : str
        The content supplied by the user to be inserted into the XML response.

    Returns
    -------
    str
        The final XML string with the escaped user content inserted into the template.
    """
    # Define the XML template with a placeholder for the escaped user content
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{user_content}</data>
</response>"""

    # Escape any special XML characters in the user content
    escaped_content = xml.sax.saxutils.escape(user_content)

    # Format the template with the escaped content
    return xml_template.format(user_content=escaped_content)