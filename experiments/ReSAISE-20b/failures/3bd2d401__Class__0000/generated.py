import html

# Predefined XML template containing a single placeholder {input_data}
xml_design = """
<response>
    <message>{input_data}</message>
</response>
"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert the user supplied content into the XML template after escaping
    characters that would otherwise interfere with XML parsing.

    Parameters:
        input_data (str): The raw content supplied by the user.

    Returns:
        str: A well‑formed XML string with the escaped content inserted.
    """
    # Escape special XML characters to prevent injection or malformed output
    safe_input = html.escape(input_data, quote=True)
    # Format the template with the sanitized content
    return xml_design.format(input_data=safe_input)