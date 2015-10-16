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
from mock import MagicMock, patch
from unittest import TestCase
from gs.group.messages.post.hide.canhide import (user_author_of_post, can_hide_post)


class TestCanPost(TestCase):

    def setUp(self):
        self.userInfo = MagicMock()
        self.userInfo.id = 'person'

    def test_user_author_of_post(self):
        post = {'author_id': self.userInfo.id}

        r = user_author_of_post(self.userInfo, post)
        self.assertTrue(r)

    def test_other_author_of_post_isnt(self):
        post = {'author_id': 'another'}

        r = user_author_of_post(self.userInfo, post)
        self.assertFalse(r)

    @patch('gs.group.messages.post.hide.canhide.user_admin_of_group')
    def test_can_hide_author(self, m_user_admin_of_group):
        'Can the author hide a post'
        m_user_admin_of_group.return_value = False
        post = {'author_id': self.userInfo.id}
        groupInfo = MagicMock()
        r = can_hide_post(self.userInfo, groupInfo, post)

        self.assertTrue(r)

    @patch('gs.group.messages.post.hide.canhide.user_admin_of_group')
    def test_can_hide_other(self, m_user_admin_of_group):
        'Is someone else prevented from hiding a post'
        m_user_admin_of_group.return_value = False
        post = {'author_id': 'other'}
        groupInfo = MagicMock()
        r = can_hide_post(self.userInfo, groupInfo, post)

        self.assertFalse(r)

    @patch('gs.group.messages.post.hide.canhide.user_admin_of_group')
    def test_can_hide_admin(self, m_user_admin_of_group):
        'Can the admin hide a post'
        m_user_admin_of_group.return_value = True
        post = {'author_id': 'other'}
        groupInfo = MagicMock()
        r = can_hide_post(self.userInfo, groupInfo, post)

        self.assertTrue(r)

    @patch('gs.group.messages.post.hide.canhide.user_admin_of_group')
    def test_can_hide_both(self, m_user_admin_of_group):
        'Can the author that is an admin hide a post'
        m_user_admin_of_group.return_value = True
        post = {'author_id': self.userInfo.id}
        groupInfo = MagicMock()
        r = can_hide_post(self.userInfo, groupInfo, post)

        self.assertTrue(r)
