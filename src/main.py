import webapp2

class Ping(webapp2.RequestHandler):
	def get(self):
		self.response.body = 'pong'


app = webapp2.WSGIApplication([
	('/s/ping', Ping)
	])
