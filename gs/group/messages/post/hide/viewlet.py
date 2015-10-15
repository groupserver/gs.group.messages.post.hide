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
from __future__ import absolute_import, division, unicode_literals, print_function
from gs.core import mailto
from gs.group.messages.post.base import PostViewlet
from .canhide import can_hide_post
from .hiddendetails import HiddenPostInfo


class HideViewlet(PostViewlet):
    @property
    def show(self):
        retval = can_hide_post(self.loggedInUser, self.groupInfo, self.manager.post)
        return retval


class HiddenPostViewlet(PostViewlet):
    '''The viewlet that shows information about posts that are hidden.'''

    #: The mailto URI, for writing email messages to support.
    MAILTO = 'mailto:{to}?subject={subject}&body={body}'

    def update(self):
        super(HiddenPostViewlet, self).update()
        postId = self.manager.post['post_id']
        self.hiddenPostInfo = HiddenPostInfo(self.context, postId)

        subject = 'Hidden post'
        b = '''Hello,

I was viewing a post that is hidden in {groupInfo.name} on
{siteInfo.name}
<{siteInfo.url}/r/post/{postId}>

and...'''
        body = b.format(groupInfo=self.groupInfo, siteInfo=self.siteInfo, postId=postId)
        self.hiddenSupportEmail = mailto(self.siteInfo.get_support_email(), subject, body)

    @property
    def show(self):
        # Use self.manager.psot because PostViewlet.update() has not been called yet
        retval = bool(self.manager.post['hidden'])
        assert type(retval) == bool, 'self.manager.post.hidden is not a Boolean'
        return retval
