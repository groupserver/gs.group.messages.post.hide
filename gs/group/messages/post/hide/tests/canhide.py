# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from mock import MagicMock
from unittest import TestCase
from gs.group.messages.post.hide.canhide import (user_author_of_post, )


class TestCanPost(TestCase):

    def setUp(self):
        pass

    def test_user_author_of_post(self):
        p = 'person'
        userInfo = MagicMock()
        userInfo.id = p
        post = {'author_id': p}

        r = user_author_of_post(userInfo, post)
        self.assertTrue(r)

    def test_other_author_of_post_isnt(self):
        userInfo = MagicMock()
        userInfo.id = 'person'
        post = {'author_id': 'another'}

        r = user_author_of_post(userInfo, post)
        self.assertFalse(r)
