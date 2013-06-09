###############################################################################
##
##  Copyright 2011-2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import sys

from twisted.internet import reactor
from twisted.python import log

from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS

from autobahn.compress import PerMessageDeflateOffer



class EchoClientProtocol(WebSocketClientProtocol):

   def onConnect(self, connectionResponse):
      print "WebSocket extensions in use: %s" % connectionResponse.extensions

   def sendHello(self):
      self.sendMessage("Hello, world!" * 100)

   def onOpen(self):
      self.sendHello()

   def onMessage(self, msg, binary):
      print "Got echo: " + msg
      reactor.callLater(1, self.sendHello)


if __name__ == '__main__':

   if len(sys.argv) < 2:
      print "Need the WebSocket server address, i.e. ws://localhost:9000"
      sys.exit(1)

   if len(sys.argv) > 2 and sys.argv[2] == 'debug':
      log.startLogging(sys.stdout)
      debug = True
   else:
      debug = False

   factory = WebSocketClientFactory(sys.argv[1],
                                    debug = debug,
                                    debugCodePaths = debug)

   factory.protocol = EchoClientProtocol

   ## Enable WebSocket extension "permessage-deflate"
   ##
   factory.setProtocolOptions(perMessageCompressionOffers = [PerMessageDeflateOffer()])

   connectWS(factory)
   reactor.run()
