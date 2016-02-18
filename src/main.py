import webapp2
import sample

class PingService(webapp2.RequestHandler):
    def get(self):
        self.response.body = '"pong"'

app = webapp2.WSGIApplication([
    ('/s/ping', PingService),
    ('/s/sample', sample.SampleService)
])
