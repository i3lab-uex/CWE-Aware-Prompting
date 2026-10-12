import xml.sax.saxutils

# Predefined XML template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_data}</message>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert the user-supplied content into an XML template.

    Parameters
    ----------
    input_data : str
        Content provided by the user to be embedded in the XML.

    Returns
    -------
    str
        The final XML string with user content safely escaped.
    """
    # Escape special XML characters to avoid injection issues.
    safe_input = xml.sax.saxutils.escape(input_data)
    return xml_design.format(input_data=safe_input)