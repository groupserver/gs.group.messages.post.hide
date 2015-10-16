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
from gs.group.messages.post.hide.viewlet import (HideViewlet, HiddenPostViewlet, )


class TestHideViewlet(TestCase):

    def setUp(self):
        self.viewlet = HideViewlet(MagicMock(), MagicMock(), MagicMock(), MagicMock())

    @patch('gs.group.messages.post.hide.viewlet.can_hide_post')
    @patch.object(HideViewlet, 'groupInfo')
    @patch.object(HideViewlet, 'loggedInUser')
    def test_show_can_hide(self, m_loggedInUser, m_groupInfo, m_can_hide_post):
        'Test that the Hide button is shown if the post is visible and we have the perms'
        m_can_hide_post.return_value = True
        self.viewlet.manager.post = {'hidden': False}
        r = self.viewlet.show

        self.assertTrue(r)

    @patch('gs.group.messages.post.hide.viewlet.can_hide_post')
    @patch.object(HideViewlet, 'groupInfo')
    @patch.object(HideViewlet, 'loggedInUser')
    def test_show_cannot_hide_perms(self, m_loggedInUser, m_groupInfo, m_can_hide_post):
        'Test that the Hide button is hidden if we lack the perms'
        m_can_hide_post.return_value = False
        self.viewlet.manager.post = {'hidden': None}
        r = self.viewlet.show

        self.assertFalse(r)

    @patch('gs.group.messages.post.hide.viewlet.can_hide_post')
    @patch.object(HideViewlet, 'groupInfo')
    @patch.object(HideViewlet, 'loggedInUser')
    def test_show_cannot_hide_hidden(self, m_loggedInUser, m_groupInfo, m_can_hide_post):
        'Test that the Hide button is hidden if the post is hidden'
        m_can_hide_post.return_value = True
        self.viewlet.manager.post = {'hidden': True}
        r = self.viewlet.show

        self.assertFalse(r)


class TestHiddenViewlet(TestCase):

    def setUp(self):
        self.viewlet = HiddenPostViewlet(MagicMock(), MagicMock(), MagicMock(), MagicMock())

    def test_show_visible(self):
        'Test that the Hidden post viewlet is hidden if the post is visible'
        self.viewlet.manager.post = {'hidden': False}
        r = self.viewlet.show

        self.assertFalse(r)

    def test_show_hidden(self):
        'Test that the Hidden post viewlet is vusuble if the post is hidden'
        self.viewlet.manager.post = {'hidden': True}
        r = self.viewlet.show

        self.assertTrue(r)

    def test_show_hidden_none(self):
        'Test that the Hidden post viewlet is hidden if the "hidden" propery is "None"'
        self.viewlet.manager.post = {'hidden': None}
        r = self.viewlet.show

        self.assertFalse(r)
