"""Controllers (the "C" in MVC): receive requests, call models, pick a view.

Each module is a Flask Blueprint for one feature area:
  main.py        home feed / search, help page
  auth.py        register, login, logout
  posts.py       create, view, edit, rate, comment, report a resource
  moderation.py  moderator dashboard and report queue
"""
