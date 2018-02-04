#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import argparse,json

import urllib.request
import tempfile
import gzip
import random

import netifaces as ni

from libtbngsetup import *

#Dictionary for random name/password geneation

Adjectives=[
'perfect','soft','hurt','zonked',
'spiritual','nondescript','ragged',
'unadvised','overconfident','ambitious','idiotic',
'bashful','guarded','elite','waggish','typical','bouncy',
'labored','placid','drab','moldy','highfalutin','maddening','imported','selfish',
'mighty','lackadaisical','redundant','parsimonious','fallacious','simplistic',
'brawny','dysfunctional','complex','stupendous','responsible','disgusting','solid',
'chemical','painful','many',
'curious','elfin','godly','rustic','classy','tidy','nappy','furtive',
'bumpy','depressed','spiky','somber','satisfying','halting','befitting',
'aloof','hateful','hot','snotty','freezing','blue-eyed','ceaseless','early'
]

Nouns=[
'statement','group','bite','school','walk','shop','toe','limit',
'gold','sort','back','lunchroom','care','view','dust','question','queen','start',
'art','ship','pencil','sugar','feeling','fruit','twig','desire','knee','elbow',
'month','jewel','toes','pocket','glass','night','cattle','place','cap','fish',
'trucks','fact','sack','rake','jail','bed','sweater','teeth','uncle','representative','sister',
'note','quill','force','board','jam',
'quarter','mouth','hate','boat','waste','coat','hat','event','chance','soup'
]

def generate_name():
  logging.debug("Generating random name")
  secure_random = random.SystemRandom()
  adjective=secure_random.choice(Adjectives)
  secure_random = random.SystemRandom()
  noun=secure_random.choice(Nouns)
  return adjective.title()+noun.title()
  

def generate_password(name):
  logging.debug("Generating random password")
  secure_random = random.SystemRandom()
  return name+str(secure_random.randint(100000, 999999))

# Gather our code in a main() function
def main(args, loglevel):

  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  logging.debug("Arguments passed: {0}".format(args))

  stubName=generate_name()
  stubPassword=generate_password(stubName)
  parameters={}
  parameters['project']=project_dir
  parameters['interface']=args.interface
 
  if args.apname is not None:
    parameters['apname']=args.apname
  else:
    parameters['apname']=stubName

  if args.appassword is not None:
    parameters['appassword']=args.appassword
  else:
    parameters['appassword']=stubPassword



  parameters['driver']=args.driver

  logging.info("Checking arguments")
  if len(parameters['appassword']) < 8:
    raise Exception("Access point password must be 8 symbols or more")

  logging.info("Checking {0} is configured manually".format(parameters['interface']))
  logging.info("Trying to get address of interface {0}".format(parameters['interface']))
  ip_address = check_interface(parameters['interface'])

  if not ip_address:
    raise Exception("Cannot determine interface {0} address. Run ifup {0} and restart the script".format(args.interface))

  filename = "{0}_hostapd.gz".format(tempfile.mktemp())
  url="http://static-bins.herokuapp.com/files/{0}/hostapd/hostapd.gz".format(args.arch)

  logging.info("""Downloading from {0}
  to {1}
  """.format(url,filename))
  urllib.request.urlretrieve(url,filename)

  logging.info("Extracting archive")
  with gzip.open(filename, "rb") as compressed_file:
    with open("{0}/bin/hostapd-tbng".format(project_dir),"wb") as uncompressed_file:
      uncompressed_file.write(compressed_file.read())
  logging.debug(utility.run_shell_command("chmod a+x {0}/bin/hostapd-tbng".format(project_dir)).decode("utf-8"))

  logging.info("Generating hostapd config file")
  filein = open("{0}/setup/templates/hostapd-tbng.conf".format(project_dir))
  src = Template( filein.read() )
  src.substitute(parameters)
  with open("{0}/config/hostapd-tbng.conf".format(project_dir), "w") as text_file:
    text_file.write(src.substitute(parameters))

  logging.info("Generating systemd file")
  systemd_folder="/lib/systemd/system"
  filein = open( "{0}/setup/templates/hostapd-tbng.service".format(project_dir))
  src = Template( filein.read() )
  src.substitute(parameters)
  with open("{0}/hostapd-tbng.service".format(systemd_folder), "w") as text_file:
    text_file.write(src.substitute(parameters))
  logging.info("File {0}/hostapd-tbng.service created".format(systemd_folder))
  logging.debug(utility.run_shell_command("systemctl daemon-reload").decode("utf-8"))
  logging.debug(utility.run_shell_command("systemctl enable hostapd-tbng").decode("utf-8")) 

  logging.debug(utility.run_shell_command("sync").decode("utf-8"))

  result="""Static version of hostapd binary installed to {0}/bin/hostapd-tbng.
Configuration located at {0}/config/hostapd-tbng.conf.
Your AP name: {3}
Your password: {4}
SystemD service hostapd-tbng is registered and enabled by default.
Don' forget to confgure dhcp service for {1} or use static IPs. Current IP of {1} is {2}""".format(
  project_dir,
  parameters['interface'],
  ip_address,
  parameters['apname'],
  parameters['appassword']
  )
  logging.info(result)


# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
  raise Exception("Python 3.x is required.")

if not os.geteuid()==0:
  raise Exception("sudo or root is required.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Script to configure static version of hostapd. Use with caution."
                                  )

  parser.add_argument('-a',
                      '--arch',
                       type=str, help='Architecture (armh,aarch64,x86,x86_64,...)',required=True)

  parser.add_argument('-i',
                      '--interface',
                       type=str, help="Interface name (wlan0,wlan1,...)",required=True)

  parser.add_argument('-n',
                      '--apname',
                       type=str, help="Access point name - will be chosen randomly, if omitted",required=False)

  parser.add_argument('-p',
                      '--appassword',
                       type=str, help="Access point password (must be 8+ symbols) - will be chosen randomly if ommitted",required=False)
  
  parser.add_argument('-d',
                      '--driver',
                      type=str, default="nl80211", help="Driver for hostapd. Default is nl80211, also possible rtl871xdrv for Realtek cards")
 
  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO

if sys.version_info[0] < 3:
  raise Exception("Python 3.x is required.")

#if not os.geteuid()==0:
#  raise Exception("sudo or root is required.")
  
main(args, loglevel)
