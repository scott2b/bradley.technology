+++
title = "django-multimail"
description = "A Django library giving one user account several email addresses, each independently verified by emailed link, without replacing Django's own User model."
weight = 9
template = "page.html"
[taxonomies]
capabilities = ["Tools"]
settings = ["Independent"]

[extra]
image = "/images/projects/django-multimail.webp"
print = "/images/projects/django-multimail-print.webp"
tagline = "Multiple verified email addresses per Django user"
place = "Python, open source"
year = "2011–2014"
+++

Django's `User` model carries one email address. People sign up with one address,
move to another, keep a work address alongside a personal one, and expect any of
them to reach them and identify them.

[django-multimail](https://github.com/scott2b/django-multimail), a library I wrote
and maintained from 2011 to 2014, added an `EmailAddress` model related to the
existing `User` and left `User` alone. It installed as an ordinary app, so a project
already on Django's authentication kept what it had and gained verified addresses.

```python
from multimail.models import EmailAddress

EmailAddress.objects.create(email='user@example.com', user=u)
# verification mail is on its way
```

## Verification

Each address has its own verified flag. Creating one sends the verification mail,
and following the link sets the flag. Saving a `User` creates an address from
`User.email`, so existing users appear in the new model with no migration.

Verification links take their domain from Django's sites framework, or from a domain
or URL set in settings. Deactivating a user deletes any addresses they never verified. An optional authentication backend lets a
user log in with any of their addresses.

## Availability

Published on PyPI as
[`django-multimail`](https://pypi.org/project/django-multimail/), MIT licensed, and
tested against Django 1.4 through 1.7. It is no longer maintained and the repository
is archived. A demo site ran at django-multimail.com, where a visitor could create an
account and watch the verification flow.

{{ figure(src="/images/projects/django-multimail-demo.webp", alt="The Multimail Demo site: a sign-up form to see multimail in action, a login form, and the five-line install recipe", caption="The demo site at django-multimail.com, as archived in January 2022. It is no longer online.") }}
