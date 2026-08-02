---
layout: page
title: Publications
---

{% for pub in site.data.publications %}

### {{ pub.year }}

{{ pub.title }}

---

{% endfor %}
