# coding=utf-8
from operator import and_
import sqlalchemy as sa
from datetime import datetime
from pytz import UTC

class PostQuery(object):
    def __init__(self, context, da):
        self.context = context
        
        self.postTable = da.createTable('post')
        self.hiddenPostTable = da.createTable('hidden_post')
        self.topicTable = da.createTable('topic')
        
    def get_hidden_post_details(self, postId):
        s = self.hiddenPostTable.select()
        s.append_whereclause(self.hiddenPostTable.c.post_id == postId)
        s.order_by(sa.desc(self.hiddenPostTable.c.date_hidden))
        
        retval = None
        r = s.execute()
        if r.rowcount >= 1:
            row = r.fetchone()
            retval = {
                'post_id':      row['post_id'],
                'date_hidden':  row['date_hidden'],
                'hiding_user':  row['hiding_user'],
                'reason':       row['reason']}
        return retval

    def hide_post(self, postId, userId, reason):
        now = datetime.now(UTC)
        self.update_post_table(postId, now)
        self.update_hidden_post_table(postId, now, userId, reason)
        
    def update_post_table(self, postId, dt):
        u = self.postTable.update(self.postTable.c.post_id == postId)
        u.execute(hidden = dt)
    
    def update_hidden_post_table(self, postId, dt, userId, reason):
        i = self.hiddenPostTable.insert()
        i.execute(post_id = postId, 
            date_hidden = dt,
            hiding_user = userId,
            reason = reason)

    def all_posts_in_topic_hidden(self, postId):
        s1 = sa.select([self.postTable.c.topic_id])
        s1.append_whereclause(self.postTable.c.post_id == postId)
        ss = s1.alias('ss')
        
        s2 = sa.select([self.postTable.c.hidden])
        s2.append_whereclause(self.postTable.c.topic_id == ss.c.topic_id)
        
        r = s2.execute()
        retval = reduce(and_, [bool(x['hidden']) for x in r], True)
        return retval
        
    def hide_topic(self, postId):
        s1 = sa.select([self.postTable.c.topic_id])
        s1.append_whereclause(self.postTable.c.post_id == postId)
        r = s1.execute()
        t = r.fetchone()['topic_id']
        
        u = self.topicTable.update(t == self.topicTable.c.topic_id)
        now = datetime.now(UTC)
        u.execute(hidden = now)
