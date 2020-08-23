# Feedly to wallabag exporter

Use this script to export your [feedly](https://feedly.com/) read_later items to [wallabag](https://www.wallabag.it).

## Getting started

### API Keys

You first need to create a develop account on feedly : [https://feedly.com/v3/auth/dev](https://feedly.com/v3/auth/dev).

Feedly will give you an ID and an `access token`. The access token will expire, do the procedure again if that's necessary.

Next in wallabag, `create a new client` in `API clients management`. This will give you a `Client ID` and a `Client secret`.

Add all those informations in `env.py`.

### Requirements

The only dependency is `requests` so you can either install it globally with `pip3 install --user requests` or use a `virtualenv`.

To create the virtualenv : `python3 -m venv venv`.

Activate it : `source venv/bin/activate`

And install the necessary libraries : `pip3 install -r requirements.txt`

### Execution

Then, execute the script : `python3 feedly_to_wallabag.py`

Done :)

---

PS: to import 194 items here's the time result : `2.76s user 0.16s system 0% cpu 4:55.29 total` so 5 minutes.
