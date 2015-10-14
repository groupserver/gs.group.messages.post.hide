===============================
``gs.group.messages.post.hide``
===============================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Hiding a post on GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-09-28
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

  ..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This product supports hiding posts that have been made to a
group. It provides both the code that hides the post and the code
that displays what appears in instead of a hidden post.

* ``gs-group-messages-post-hide-action`` is the *viewlet* that
  provides the button that hides the post.
* ``hide_post.ajax`` is the AJAX "page" that supplies the form
  that hides a post.
* ``gs-group-messages-post-hide-hidden`` is the viewlet that is
  displayed when a post is hidden.
* ``hide-post-20110415.js`` is the JavaScript resource that
  supports hiding a post.

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.group.messages.post.hide/
- Translations:
  https://www.transifex.com/groupserver/gs-group-messages-post-hide/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
