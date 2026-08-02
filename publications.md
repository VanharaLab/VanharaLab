---
layout: page
title: Publications
---

# Publications

{% for pub in site.data.publications %}

### {{ pub.year }}

**{{ pub.title }}**

{% if pub.journal %}
*{{ pub.journal }}*
{% endif %}

{% if pub.doi %}
[DOI]({{ pub.doi }})
{% endif %}

---

{% endfor %}
