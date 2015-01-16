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

print "***** This shell does not mount the files system of the running app. ******"
print "***** You cannot see the log files from the running container.       ******"
print "***** Use this shell to run rails consoles or rake tasks.            ******"
input=raw_input("Start shell to %s/%s from %s:%s. Continue [Y/n]? " % (rails_env, target, docker_repo, tag))
if input == 'n': 
    print "Aborted."
    sys.exit()

cmd = 'sudo docker run -t -i --rm -e RAIL_ENV=%s --name shell-no-mount-%s %s:%s /bin/bash' % (rails_env, executable_container_name, docker_repo, tag)

print "Running '%s'" % cmd
os.system(cmd)


