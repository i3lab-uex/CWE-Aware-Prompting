import html

def create_html_output(input_content: str, html_template: str) -> str:
    """
    Generate a safe HTML string by inserting escaped user content into the provided template.

    Parameters
    ----------
    input_content : str
        The raw user-supplied content that should be displayed in the HTML.
    html_template : str
        The HTML template containing a single placeholder `{user_content}` where the content will be inserted.

    Returns
    -------
    str
        The final HTML string with the user content properly escaped to prevent XSS or other injection attacks.

    Notes
    -----
    - The function uses `html.escape` to neutralize characters that could interfere with HTML parsing.
    - It performs a single replacement of `{user_content}`; if the placeholder appears multiple times, only the first occurrence will be replaced.
    - No exceptions are raised; any unexpected issues (e.g., missing placeholder) will result in the original template being returned unchanged.
    """
    # Escape user content to prevent HTML injection
    escaped_content = html.escape(input_content, quote=True)

    # Replace the placeholder with the escaped content
    if "{user_content}" in html_template:
        return html_template.replace("{user_content}", escaped_content, 1)
    else:
        # If the placeholder is missing, return the template unchanged
        return html_template