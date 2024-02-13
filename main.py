"""main.py

Define the Jinja2 variables, macros and filters for extensions components in Mkdocs.
"""

mapping_header_background = {
    "GET": "#ECF3FC",
    "POST": "#E7F6EF",
    "PUT": "#FBF2E7",
    "DELETE": "#F9E7E6",
    "PATCH": "#F0E6FA",
    "OPTIONS": "#F0E6FA",
    "HEAD": "#F0E6FA",
}

mapping_border_background = {
    "GET": "#61AFFD",
    "POST": "#4ACC91",
    "PUT": "#F8A132",
    "DELETE": "#F53E3D",
    "PATCH": "#9027FB",
    "OPTIONS": "#9027FB",
    "HEAD": "#9027FB",
}

mapping_badge_background = {
    "GET": "#61AFFD",
    "POST": "#4ACC91",
    "PUT": "#F8A132",
    "DELETE": "#F53E3D",
    "PATCH": "#9027FB",
    "OPTIONS": "#9027FB",
    "HEAD": "#9027FB",
}

set_card_header_style = lambda verb_http: f"""
background-color: {mapping_header_background[verb_http]} !important;
border-color: {mapping_border_background[verb_http]} !important;
border: 1px solid {mapping_border_background[verb_http]} !important;
"""

set_card_badge_style = lambda verb_http: f"""
background-color: {mapping_badge_background[verb_http]} !important;
"""

set_collapsable_card_style = lambda verb_http: f"""
border-color: {mapping_header_background[verb_http]} !important;
"""

set_card_body_style = lambda verb_http: f"""
border-bottom: 1px solid {mapping_border_background[verb_http]} !important;
border-left: 1px solid {mapping_border_background[verb_http]} !important;
border-right: 1px solid {mapping_border_background[verb_http]} !important;
"""

set_chevron_style = lambda verb_http: f"""
color: {mapping_border_background[verb_http]} !important;
background-color: {mapping_header_background[verb_http]} !important;
"""


def define_env(env) -> None:
    """
    Hook for macros, variables and filters plugins.

    :param env: the Jinja2 environment.
    :type env: jinja2.environment.Environment
    :return: None
    :rtype: None
    """

    @env.macro
    def macro_collapse_card_api_doc(verb_http: str, url: str) -> str:
        """Macro to create a custom HTML collapsable card for the API documentation in Markdown files.

        :param verb_http: verb of the HTTP request (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD).
        :type verb_http: str
        :param url: URL of the API endpoint.
        :type url: str
        :return: the HTML collapsable card for the API documentation.
        :rtype: str
        """
        verb_http = verb_http.upper()
        return f"""
<div class="collapse-card" data-url="{url}" style="{set_collapsable_card_style(verb_http=verb_http)}">
    <div class="card-header" style="{set_card_header_style(verb_http=verb_http)} !important;" onclick="toggleCollapse(this)">
        <span class="badge" style="{set_card_badge_style(verb_http=verb_http)}">{verb_http}</span>
        <span class="title-header">{url}</span>
        <span class="chevron" style="{set_chevron_style(verb_http=verb_http)}"></span>
    </div>
    <div class="card-body" style="{set_card_body_style(verb_http=verb_http)}">
    </div>
</div>
      """
