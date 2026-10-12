import xml.sax.saxutils

# Example XML design with a placeholder for user content.
xml_design = """
<response>
    <message>{input_data}</message>
</response>
"""

def process_xml_reply(input_data: str) -> str:
    """
    Inserts user-supplied content into the predefined XML template.

    Parameters
    ----------
    input_data : str
        The content submitted by the user that will be placed into the XML template.

    Returns
    -------
    str
        The final XML response with user content included at the appropriate position in the template.
    """
    # Escape the input to avoid XML injection and ensure well‑formedness
    safe_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", '"': "&quot;"})
    # Format the XML design with the escaped input
    return xml_design.format(input_data=safe_input)