#!/usr/bin/python

import sys
import readline
import SOAPpy
import getpass
import ConfigParser

from optparse import OptionParser

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()

config = ConfigParser.RawConfigParser()
config.read('vimu.cfg')

# Writing our configuration file to 'example.cfg'
with open('example.cfg', 'wb') as configfile:
    config.write(configfile)

parser = OptionParser('usage: %prog [options]')
parser.add_option("-p", "--project", dest="project", help="project key, ex: PANELCELL")
parser.add_option('-n', '--number', type = 'int', dest='issue_number', help="issue number, ex: 213")
parser.add_option('-f', '--from', type = 'string', dest='from_status', help="from status of issue(s)")
parser.add_option('-t', '--to', type = 'string', dest='to_status', help="to status of issue(s)")

(options, argv) = parser.parse_args()

if options.project == None:
    parser.print_usage()
    exit('-p parameter is must to use')
if options.from_status == None:
    parser.print_usage()
    exit('-f parameter is must to use')
if options.to_status == None:
    parser.print_usage()
    exit('-t parameter is must to use')
if options.issue_number == None:
    parser.print_usage()
    exit('-n parameter is must to use')

print 'Jira Authentication'
username = rlinput('enter username: ', getpass.getuser())
password = getpass.getpass("enter password for user %s: " % username, sys.stderr)
wsdl = rlinput('enter service wsdl: ', config.get('main', 'jira_wsdl'))

print 'Username: ' + username
print 'Password: ******'
print 'Service : ' + wsdl

soap = SOAPpy.WSDL.Proxy(wsdl)
auth = soap.login(username, password)

print "Successfully completed authentication: " + auth
print 

issue = soap.getIssue(auth, options.project + '-' + str(options.issue_number))
print "      issue: " + issue.key
print "description: " + issue.description
print "     status: " + issue.status
