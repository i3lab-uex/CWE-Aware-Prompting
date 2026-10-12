import html

def generate_xml_response(user_content: str) -> str:
    """
    Generate a well‑formed XML response by embedding the user provided content
    into a predefined template. The user content is properly escaped to avoid
    XML injection or malformed documents.

    Args:
        user_content (str): The content supplied by the user that will be
                            inserted into the XML response.

    Returns:
        str: The fully formed XML string with the user content safely embedded.
    """
    # Escape characters that have special meaning in XML
    safe_content = html.escape(user_content, quote=True)

    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <message>{user_content}</message>\n'
        '</response>'
    )

    return xml_template.format(user_content=safe_content)