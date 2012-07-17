# coding=utf-8
from zope.publisher.interfaces import NotFound
from zope.formlib import form
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.security.interfaces import Unauthorized
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('groupserver')
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFMailingListManager.queries import MessageQuery
from gs.group.base.form import GroupForm
from interfaces import IHide
from queries import PostQuery
from canhide import can_hide_post

class HidePost(GroupForm):
    form_fields = form.Fields(IHide)
    label = _(u'Hide a Post')
    pageTemplateFileName = 'browser/templates/hide.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        GroupForm.__init__(self, context, request)
         self.can_hide_post = can_hide_post

    @form.action(label=_('Hide'), failure='handle_failure')
    def handle_hide(self, action, data):
        postInfo = self.get_post(data['postId'])
        if not(self.can_hide_post(self.loggedInUser, self.groupInfo, postInfo)):
            # Do not try and hack the URL.
            m = 'You are not allowed to hide the post %s in %s (%s)' %\
                (data['postId'], self.groupInfo.name, self.groupInfo.id)
            raise Unauthorized(m)
        self.postQuery.hide_post(data['postId'], self.loggedInUser.id, 
                                    data['reason'])
        if self.postQuery.all_posts_in_topic_hidden(data['postId']):
            self.postQuery.hide_topic(data['postId'])
        self.status = u'Hidden the post.'
        uri = '/r/topic/%s#post-%s' % (data['postId'], data['postId'])
        self.request.RESPONSE.redirect(uri)
    
        # --=mpj17=-- There is a potential for an information leak with
        # post hiding. If the post is hidden and the topic contains a
        # visible post then the contents of the hidden post can be
        # determined by doing a series of searches: if the topic comes
        # up and the keyword in not in any of the visible posts then it
        # must be in the hidden post. Lets consider fixing this issue
        # when we deal to Ticket 224: Optimise Search Performance
        # <https://projects.iopen.net/groupserver/ticket/224>.
    
    def handle_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _(u'<p>There is an error:</p>')
        else:
            self.status = _(u'<p>There are errors:</p>')

    @Lazy
    def postQuery(self):
        assert self.context
        da = self.context.zsqlalchemy
        assert da
        retval = PostQuery(self.context, da)
        assert retval
        return retval

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        assert retval
        assert not(retval.anonymous), 'Anon trying to hide a post!'
        return retval

    @Lazy
    def messageQuery(self):
        assert self.context, 'No context for a post!'
        da = self.context.zsqlalchemy 
        assert da, 'No data-adaptor found'
        retval = MessageQuery(self.context, da)
        assert retval
        return retval

    def get_post(self, postId):
        retval = self.messageQuery.post(postId)
        if not retval:
          raise NotFound(self, postId, self.request)
        if retval['group_id'] != self.groupInfo.id:
            m = u'You are not authorized to access this post from '\
                'the group %s' % self.groupInfo.name
            raise Unauthorized(m)
        assert retval
        return retval

