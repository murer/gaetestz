import webutil

from google.appengine.ext import ndb

class SampleEntity(ndb.Model):
    desc = ndb.StringProperty()
    num = ndb.IntegerProperty()

class SampleService(webutil.BaseHandler):

    def get(self):
        ident = self.param('id')
        ret = SampleEntity.get_by_id(ident)
        if not ret:
            raise webutil.NotFoundError()
        self.resp_json({ 'id': ret.key.id(), 'desc': ret.desc, 'num': ret.num })

    def post(self):
        data = self.req_json()
        ent = SampleEntity(id = data['id'], 
            desc = data.get('desc'),
            num = data.get('num'))
        ret = ent.put()
        self.resp_json({
            'kind': ret.kind(),
            'id': ret.id()
        })

    def delete(self):
        ident = self.param('id')
        ret = ndb.Key("SampleEntity", ident)
        ret.delete()
        self.resp_json({
            'kind': ret.kind(),
            'id': ret.id()
        })

