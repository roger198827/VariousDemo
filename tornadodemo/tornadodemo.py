from operator import mul
import tornado.ioloop
import tornado.web
import string
import time
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from flasky import app

def P(x,y=None):
    if x==0 or y==0:
        return 1
        re=x
        i=x-1
        if y==None:
            z=1
        else:
            z=x-y
            while i>z:
                re *=i
                i -=1
                return re

def P2(n):
    print reduce(lambda x,y:x*y, range(1,n+1))

def P3(n):
    print reduce(mul, range(1,n+1))

def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)
def fra(n):
    if n < 1:
        return 1
    i = 1
    total = 1
    while i <= n:
        total *= i
        i += 1
        continue
    return total
    
def make_repeater(n):
    return lambda s: s*n

twice = make_repeater(2)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello Tornado")
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        fp=open("log.log", "a+")
        print >> fp, "access 192.168.204.126:8888"
        print "access 192.168.204.126:8888\n"
        fp.close()
        def post(self):
            self.set_header("Content-Type", "text/plain")
            self.write("You wrote "+ self.get_argument("message"))
            message=self.get_argument("message")
            res=P(string.atoi(message))
            clientinfo=repr(self.request)
            fp=open("log.log", "a+")
            print >> fp, "access 192.168.204.126:8888/story with param message : %s" % message
            print "access 192.168.204.126:8888/story with param message : %s\n" % message
            print "P(x) of %s, is %d" % (message, res)
            P2(string.atoi(message))
            P3(string.atoi(message))
            #print "Client Info : %s" % clientinfo
            fp.close()

class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You request the story "+story_id)

class FunnyHandler(tornado.web.RequestHandler):
    def get(self, funny_id):
        self.write("You funny request the story "+funny_id)
        print twice('word')
        print twice(5)

class FacHandler(tornado.web.RequestHandler):
    def get(self, fac_id):
        self.write("Fac ID is:"+fac_id)
        print "http request from Client IP: %s" % self.request.remote_ip
        ticks=time.time()
        print "Before call fac function : ", ticks
        print "Fac ID is:%s" % fac_id
        print "Fac result : %r" % factorial(string.atoi(fac_id))
        ticks=time.time()
        print "After call fac function : ", ticks

tr = WSGIContainer(app)
        
application=tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/([0-9])+", StoryHandler),
    (r"/funny/([0-9])+", FunnyHandler),
    (r"/fac/([0-9])+", FacHandler),
    (r"/.*", FallbackHandler, dict(fallback=tr)),    
])

if __name__=="__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
