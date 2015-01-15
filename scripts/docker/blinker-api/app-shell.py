#!/usr/bin/python

import sys, os, datetime

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

ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
executable_container_name='%s-%s-%s' % (target, tag, ts)
data_container_name='%s-%s-data' % (target, tag)

input=raw_input("Start shell to %s/%s from %s:%s. Continue [Y/n]? " % (rails_env, target, docker_repo, tag))
if input == 'n':
    print "Aborted."
    sys.exit()

cmd = 'sudo docker run -t -i --rm -e RAILS_ENV=%s --volumes-from %s --name shell-%s %s:%s /bin/bash' % (rails_env, data_container_name, executable_container_name, docker_repo, tag)

print "Running '%s'" % cmd
os.system(cmd)


