#!/usr/bin/python

import sys, os

target="blinker-api"
docker_repo="blinker/blinker-api"
rails_env="staging"
environments = ("development", "integration", "staging", "production")

tag=raw_input("Enter tag for docker hub repo %s? " % docker_repo)

input=raw_input("RAILS_ENV=(%s)? [%s]: " % ('|'.join(environments), rails_env))
if input != "":
    if input in environments:
        rails_env = input
    else:
        print "Environment must be (%s)" % '| '.join(environments)
        sys.exit()
else:
    input = "staging"
    

executable_container_name='%s-%s' % (target, tag)
data_container_name='%s-data' % executable_container_name
data_container_command="echo %s/%s" % (rails_env, data_container_name)

input=raw_input("Stop blinker-api and its data-only container in %s/%s, from %s:%s. Continue [Y/n]? " % (rails_env, target, docker_repo, tag))
if input == 'n': 
    print "Aborted."
    sys.exit()

print '''

STOPPING RUNNING CONTAINER =======================================================================================
Executable container: %s
''' % (executable_container_name)
cmd="sudo docker stop %s" % executable_container_name
print "Running %s" % cmd
os.system(cmd)

clean = raw_input("Remove the containers?  You won't have access to the logs after containers are purged. [Y/n]: ")
if clean == "n" or (clean != "" and clean != "Y"):
    print "Done, without removing containers."
    sys.exit()

print '''

CLEANING UP CONTAINERS ============================================================================================
Executable and data-only containers: %s, %s
''' % (executable_container_name, data_container_name)
cmd="sudo docker rm %s %s" % (executable_container_name, data_container_name)
print "Running %s" % cmd
os.system(cmd)




