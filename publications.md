---
layout: page
title: Publications
---

## Publications

{% raw %}
{% for pub in site.data.publications %}

### {{ pub.year }}

{{ pub.title }}

---

{% endfor %}
{% endraw %}
