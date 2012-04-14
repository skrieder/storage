import cgi
import datetime
import logging
import StringIO

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

logging.getLogger().setLevel(logging.DEBUG)


class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
    def get(self):
      self.response.out.write("<html><body>")
      greetings = self.get_greetings()
      stats = memcache.get_stats()

      self.response.out.write("<b>Cache Hits:%s</b><br>" % stats['hits'])
      self.response.out.write("<b>Cache Misses:%s</b><br><br>" %
                              stats['misses'])
      self.response.out.write(greetings)
      self.response.out.write("""
            <form action="/sign" method="post">
              <div><textarea name="content" rows="3" cols="60"></textarea></div>
              <div><input type="submit" value="Sign Guestbook"></div>
            </form>
          </body>
        </html>""")

    def get_greetings(self):
        """
        get_greetings()
        Checks the cache to see if there are cached greetings.
        If not, call render_greetings and set the cache

        Returns:
           A string of HTML containing greetings.
        """
        greetings = memcache.get("greetings")
        if greetings is not None:
            return greetings
        else:
            greetings = self.render_greetings()
            if not memcache.add("greetings", greetings, 10):
                logging.error("Memcache set failed.")
            return greetings

    def render_greetings(self):
        """
        render_greetings()
        Queries the database for greetings, iterate through the
        results and create the HTML.

        Returns:
           A string of HTML containing greetings
        """
        results = db.GqlQuery("SELECT * "
                              "FROM Greeting "
                              "ORDER BY date DESC").fetch(10)
        output = StringIO.StringIO()
        for result in results:
            if result.author:
                output.write("<b>%s</b> wrote:" % result.author.nickname())
            else:
                output.write("An anonymous person wrote:")
            output.write("<blockquote>%s</blockquote>" %
                         cgi.escape(result.content))
        return output.getvalue()

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')


application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
