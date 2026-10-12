import re
from html import escape

def render_html_template(html_template: str, input_map: dict) -> str:
    """
    Render an HTML template by replacing placeholders with user-provided values.

    Parameters
    ----------
    html_template : str
        The HTML template containing placeholders in the form `{placeholder}`.
    input_map : dict
        A mapping from placeholder names to values that should replace them.

    Returns
    -------
    str
        The resulting HTML string with all placeholders replaced by escaped values.

    Raises
    ------
    ValueError
        If a placeholder in the template does not have a corresponding entry in `input_map`,
        or if any other error occurs during rendering.
    """
    # Pattern to match placeholders like {name}
    placeholder_pattern = re.compile(r'\{(\w+)\}')

    def _replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in input_map:
            raise ValueError(f"Missing value for placeholder: '{key}'")
        # Escape the user-provided value to avoid XSS or HTML injection
        return escape(str(input_map[key]))

    try:
        rendered = placeholder_pattern.sub(_replace, html_template)
    except re.error as exc:
        raise ValueError(f"Invalid regular expression used in template processing: {exc}") from exc
    except Exception as exc:
        # Catch any unexpected exception and wrap it in ValueError for consistency
        raise ValueError(f"An error occurred while rendering the template: {exc}") from exc

    return rendered