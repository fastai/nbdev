{%- extends 'markdown.tpl' -%}

{% block input_group -%}
{%- if cell.metadata.collapse_show -%}
<details class="description" open>
    <summary>Code details ...</summary>
    {{ super() }}
</details>
{{ '' }}
{%- elif cell.metadata.collapse_hide -%}
<details class="description">
    <summary>Code details ...</summary>
    {{ super() }}
</details>
{{ '' }}
{%- elif cell.metadata.hide_input or nb.metadata.hide_input -%}
{%- else -%}
    {{ super() }}
{%- endif -%}
{% endblock input_group %}

{% block output_group -%}
{%- if cell.metadata.hide_output -%}
{%- elif cell.metadata.collapse_output -%}
<details class="description">
    <summary>Output details ...</summary>
    {{ super() }}
</details>
{{ '' }}
{%- else -%}
    {{ super() }}
{%- endif -%}
{% endblock output_group %}