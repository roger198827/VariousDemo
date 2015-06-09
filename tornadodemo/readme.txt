0. Change your Own IP before run both in testThreading.py & tornadodemo.py
1. Flask(block) + Tornado(non-block)
   a) open browser, input "IP:8888/flask"
   b) browser will show "This comes from Flask ^_^"
   c) console will show "
   "######
   720
   Calc Fac in Flask, result : 720
   "######
flasky.py:
###############################################
def P2(n):
    print reduce(lambda x,y:x*y, range(1,n+1))
    return reduce(lambda x,y:x*y, range(1,n+1))

@app.route('/flask')
def hello_world():
    print 'Calc Fac in Flask, result : %d'%P2(6)
    return 'This comes from Flask ^_^'
###############################################
Tornado:
###############################################
#import app
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

###############################################
2. Multi-Thread Call from HTTP Sync Client
   a) run "python tornadodemo.py"
   b) run "python testThreading.py"
demo will auto gen int from 5 to 15, and calc result in tornadodemo server
   c) modify thread number and interval time to what you want to check the different result
###############################################

###############################################
3. Using AsyncHttpClient and different fac function (not test yet)
