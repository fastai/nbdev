{%- extends 'hide-md.tpl' -%}{% block body %}
{% if resources.title != "" and resources.title != nil %}# {{resources.title}}{% endif %}
{% if resources.summary != "" and resources.summary != nil %}> {{resources.summary}}{% endif %}

{{ super() }}
{%- endblock body %}

