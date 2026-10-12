import html

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML response by safely inserting user-supplied content into a
    predefined template.

    Parameters:
        input_content (str): Text supplied by the user that will be embedded in
                             the XML structure.

    Returns:
        str: The complete XML string with the escaped user content.
    """
    # Predefined XML template with a placeholder for user content
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <data>{input_content}</data>\n'
        '</response>'
    )

    # Escape special XML characters to prevent injection and ensure well‑formedness
    safe_content = html.escape(input_content, quote=True)

    # Insert the escaped content into the template
    return xml_template.format(input_content=safe_content)