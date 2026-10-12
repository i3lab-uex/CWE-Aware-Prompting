import html

# Template with a placeholder for user content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generates an XML response by safely embedding user-provided content into
    a predefined template.

    Parameters:
        user_content (str): The content supplied by the user to be included
                            in the XML.

    Returns:
        str: The fully formed XML string with user content properly escaped.
    """
    # Escape special XML characters to prevent injection attacks
    safe_content = html.escape(user_content, quote=True)

    # Construct the final XML using the escaped content
    return xml_template.format(user_content=safe_content)