import xml.sax.saxutils

# Define the XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the user-provided content into a template.
    
    Args:
        user_content (str): The user-provided content to be embedded into the XML response.
    
    Returns:
        str: The generated XML response incorporating the user-provided content.
    
    Notes:
        - Special characters in `user_content` are escaped to prevent XML injection.
        - No exceptions are raised explicitly; any encoding errors will propagate naturally.
    """
    # Escape XML special characters in the user content to avoid injection or malformed XML
    escaped_content = xml.sax.saxutils.escape(user_content, entities={"'": "&apos;", "\"": "&quot;"})
    
    # Format the template with the escaped content
    return xml_template.format(user_content=escaped_content)