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

executable_container_command="zkstart -root=/environments/integration -stdout -newline bundle exec unicorn -p 3000 -c ./config/unicorn.rb --no-default-middleware"
docker_ports_options="-P"
docker_ntp_options="-v /etc/localtime:/etc/localtime:ro"

input=raw_input("Launch blinker-api mounting file system on a data-only container in %s/%s, from %s:%s. Continue [Y/n]? " % (rails_env, target, docker_repo, tag))
if input == 'n': 
    print "Aborted."
    sys.exit()


print '''

CONTAINER 1 =========================================================================================
Data-only container: %s ==> mountable filesystems.
''' % data_container_name
cmd="sudo docker run -d -e RAILS_ENV=%s --name %s %s:%s %s" % (rails_env, data_container_name, docker_repo, tag, data_container_command)
print "Running %s" % cmd
os.system(cmd)

print '''


CONTAINER 2 =========================================================================================
Executable container: %s ==> %s
''' % (executable_container_name, executable_container_command)
cmd="sudo docker run -d --name %s --volumes-from %s %s %s -e RAILS_ENV=%s %s:%s %s" %(executable_container_name, data_container_name, docker_ports_options, docker_ntp_options, rails_env, docker_repo, tag, executable_container_command)
print "Running %s" % cmd
os.system(cmd)

os.system("sudo docker ps -a")
