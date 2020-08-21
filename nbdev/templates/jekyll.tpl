{%- extends 'hide.tpl' -%}{% block body %}---
{% if resources.toc != "" and resources.toc != nil %}toc: {{resources.toc}}{% endif %}
{% if resources.title != "" and resources.title != nil %}title: {{resources.title}}{% endif %}
{% if resources.image != "" and resources.image != nil %}image: {{resources.image}}{% endif %}
{% if resources.hide_colab_badge != "" and resources.hide_colab_badge != nil %}hide_colab_badge: {{resources.hide_colab_badge}}{% endif %}
keywords: {{resources.keywords}}
sidebar: home_sidebar
{% if resources.tags != "" and resources.tags != nil %}tags: {{resources.tags}}{% endif %}
{% if resources.summary != "" and resources.summary != nil %}summary: "{{resources.summary}}"{% endif %}
{% if resources.summary != "" and resources.summary != nil %}description: "{{resources.summary}}"{% endif %}
{% if resources.nb_path != "" and resources.nb_path != nil %}nb_path: "{{resources.nb_path}}"{% endif %}
---
{% include 'autogen.tpl' %}

<div class="container" id="notebook-container">
        {{ super()  }}
</div>
{%- endblock body %}
