---
layout: page
title: Publications
---

## Publications


{% for pub in site.data.publications %}

### {{ pub.year }}

{{ pub.title }}

---

{% endfor %}
{% endraw %}
