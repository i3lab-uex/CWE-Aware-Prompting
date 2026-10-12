import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Insert user-provided content into an HTML template safely.

    Parameters
    ----------
    input_text : str
        Text supplied by the user to be embedded in the template.
    html_template : str
        HTML structure containing a single placeholder `{user_content}`.

    Returns
    -------
    str
        The HTML string with the user content safely escaped and inserted.

    Notes
    -----
    * Uses ``html.escape`` to neutralize any HTML/JS injection attempts.
    * If the template contains multiple `{user_content}` placeholders,
      all will be replaced.  If none exist, the function returns the
      original template unchanged.
    """
    # Escape user content to prevent XSS or injection attacks
    escaped_content = html.escape(input_text, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.replace("{user_content}", escaped_content)