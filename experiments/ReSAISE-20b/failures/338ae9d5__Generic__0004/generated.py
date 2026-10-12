import html

# Pre‑defined XML template with a placeholder for user input.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_content}</content>
</response>"""

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting the user supplied content into
    a predefined template. The input is escaped to prevent XML injection.

    Parameters:
        input_content (str): Text supplied by the user.

    Returns:
        str: The constructed XML response with the escaped content.
    """
    # Escape special XML characters to avoid injection issues
    safe_content = html.escape(input_content, quote=True)
    # Format the template with the escaped content
    return xml_template.format(input_content=safe_content)