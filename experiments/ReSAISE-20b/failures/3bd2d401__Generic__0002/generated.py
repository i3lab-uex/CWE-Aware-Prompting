import xml.sax.saxutils

# Example XML template containing a placeholder {input_data}
xml_design = """
<response>
    <message>{input_data}</message>
</response>
"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert user supplied content into an XML template.

    Parameters
    ----------
    input_data : str
        The raw string entered by the user.  It will be escaped to avoid XML injection.

    Returns
    -------
    str
        The final XML string with the escaped user content inserted at the placeholder.
    """
    # Escape special XML characters in the user input
    safe_input = xml.sax.saxutils.escape(input_data)

    # Format into the template; no other formatting is performed
    return xml_design.format(input_data=safe_input)