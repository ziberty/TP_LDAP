#import logging

#from flask import Flask, abort, request, render_template, redirect, url_for

#logging.basicConfig(level=logging.INFO)

#app = Flask(__name__)


#@app.route("/", methods=["GET"])
#def home():
#    vlilles = Vlille.query.order_by(Vlille.nom).offset(0).limit(20)

#    return render_template("vlille.html", vlilles=vlilles)

import sys
import io

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.inmemory import fromLDIFFile
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)


LDIF = b"""\
dn: dc=org
dc: org
objectClass: dcObject

dn: dc=example,dc=org
dc: example
objectClass: dcObject
objectClass: organization

dn: ou=people,dc=example,dc=org
objectClass: organizationalUnit
ou: people

dn: cn=bob,ou=people,dc=example,dc=org
cn: bob
gn: Bob
mail: bob@example.org
objectclass: top
objectclass: person
objectClass: inetOrgPerson
sn: Roberts
userPassword: secret

dn: gn=John+sn=Doe,ou=people,dc=example,dc=org
objectClass: addressbookPerson
gn: John
sn: Doe
street: Back alley
postOfficeBox: 123
postalCode: 54321
postalAddress: Backstreet
st: NY
l: New York City
c: US
userPassword: terces

dn: gn=John+sn=Smith,ou=people, dc=example,dc=org
objectClass: addressbookPerson
gn: John
sn: Smith
telephoneNumber: 555-1234
facsimileTelephoneNumber: 555-1235
description: This is a description that can span multi
 ple lines as long as the non-first lines are inden
 ted in the LDIF.
userPassword: eekretsay

"""


class Tree:
    def __init__(self):
        global LDIF
        self.f = io.BytesIO(LDIF)
        d = fromLDIFFile(self.f)
        d.addCallback(self.ldifRead)

    def ldifRead(self, result):
        self.f.close()
        self.db = result


class LDAPServerFactory(ServerFactory):
    protocol = LDAPServer

    def __init__(self, root):
        self.root = root

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.debug = self.debug
        proto.factory = self
        return proto

def addLdapUser(cn, sn, email, userPassword, ou):
    #cryptMsg = fernet.encrypt(testData.encode())
    #decryptMsg = fernet.decrypt(cryptMsg).decode()

    cn = fernet.encrypt(cn.encode())
    userPassword = fernet.encrypt(userPassword.encode())

    dnString = "\n\ndn: cn=" + str(cn) + ",ou=" + ou + ",dc=example,dc=org"
    cnString = "\n cn: " + str(cn)
    snString = "\n sn: " + sn
    emailString = "\n email: " + email
    userPasswordString = "\n userPassword: " + str(userPassword)
    string = dnString + cnString + snString + emailString + userPasswordString
    stringLDIF = LDIF + str.encode(string)
    return stringLDIF


if __name__ == "__main__":
    from twisted.internet import reactor

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8080
    # First of all, to show logging info in stdout :
    log.startLogging(sys.stderr)
    # We initialize our tree
    tree = Tree()
    # When the LDAP Server protocol wants to manipulate the DIT, it invokes
    # `root = interfaces.IConnectedLDAPEntry(self.factory)` to get the root
    # of the DIT.  The factory that creates the protocol must therefore
    # be adapted to the IConnectedLDAPEntry interface.
    registerAdapter(lambda x: x.root, LDAPServerFactory, IConnectedLDAPEntry)
    factory = LDAPServerFactory(tree.db)
    factory.debug = True
    application = service.Application("ldaptor-server")
    myService = service.IServiceCollection(application)
    serverEndpointStr = f"tcp:{port}"
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)
    reactor.run()
