#!/usr/bin/python

import sys, os

target="blinker-api"
docker_repo="blinker/blinker-api"
rails_env="staging"
environments = ("staging", "production")

tag=raw_input("Enter tag for docker hub repo %s? " % docker_repo)

input=raw_input("RAILS_ENV=(%s)? [%s]: " % ('|'.join(environments), rails_env))
if input != "":
    if input in ("staging", "production"):
        rails_env = input
    else:
        print "Environment must be (%s)" % '| '.join(environments)
        sys.exit()
else:
    input = "staging"
    

executable_container_name='%s-%s' % (target, tag)
data_container_name='%s-data' % executable_container_name

input=raw_input("Tail the log of %s/%s from %s:%s. Continue [Y/n]? " % (rails_env, target, docker_repo, tag))
if input == 'n': 
    print "Aborted."
    sys.exit()

cmd = 'sudo docker run -t -i --rm -e RAIL_ENV=%s --volumes-from %s --name tail-logs-%s %s:%s tail -f log/%s.log' % (rails_env, data_container_name, executable_container_name, docker_repo, tag, rails_env)

print "Running '%s'" % cmd
os.system(cmd)


