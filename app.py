import sys

import pyForms
import tornado


#web server
import webpages.index
myFirstWebpage = pyForms.Page(webpages.index.controller)

import webpages.control
controlPage = pyForms.Page(webpages.control.controller)

#START WEB SERVERY STUFF
import tornado.ioloop
import tornado.web

application = tornado.web.Application([
    (r"/", pyForms.tornadoHandler(myFirstWebpage)),
    (r"/control", pyForms.tornadoHandler(controlPage)),
])

portNumber = sys.argv[1] if len(sys.argv) > 1 else 8888
application.listen(portNumber)
tornado.ioloop.IOLoop.instance().start()




