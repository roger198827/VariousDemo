import tornado
import tornado.ioloop
import threading
import time
import random
from tornado.httpclient import *
from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from flasky import app


class timer(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self): #Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            print 'Thread Object(%d), Start Time:%s\n' %(self.thread_num, time.ctime())
            http_client = tornado.httpclient.HTTPClient()
            try:
                url='http://127.0.0.1:8888/fac/'+str(random.randint(5, 26))
                response = http_client.fetch(url)
                print 'Thread Ojbect(%d), response body: %s' %(self.thread_num,response.body)
            except tornado.httpclient.HTTPError, e:
                print "Error:", e
            print 'Thread Object(%d), End Time:%s\n' %(self.thread_num, time.ctime())
        time.sleep(self.interval)
    def stop(self):
        self.thread_stop = True

def test():
    thread1 = timer(1, 1)
    thread2 = timer(2, 2)
    thread1.start()
    thread2.start()
    time.sleep(10)
    thread1.stop()
    thread2.stop()
    return

if __name__ == '__main__':
    test()