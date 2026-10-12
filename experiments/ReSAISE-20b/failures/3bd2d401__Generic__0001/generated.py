import xml.sax.saxutils

# The XML template with a placeholder for user content.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_data}</message>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert the user-provided content into the XML template safely.

    Parameters
    ----------
    input_data : str
        The raw content supplied by the user.

    Returns
    -------
    str
        The XML document with the user's content inserted, with all
        special characters escaped to prevent malformed XML or injection.
    """
    # Escape any XML-special characters in the user input
    safe_content = xml.sax.saxutils.escape(input_data)

    # Format the template with the escaped content
    return xml_design.format(input_data=safe_content)