# A different approach

This approach uses container to container communication. This requires that the bug in /overleaf/services/web/app/src/Features/User/UserRegistrationHandler.js is fixed. see https://github.com/overleaf/overleaf/issues/1206

EmailHandler.promises.sendEmail('registered', { 

is missing an await. 

await EmailHandler.promises.sendEmail('registered', { 

I fixed the file out side an mount it in the overleaf compose.yaml via
    volumes:
      - /root/overleafserver/UserRegistrationHandler.js:/overleaf/services/web/app/src/Features/User/UserRegistrationHandler.js

# More restrictive

We can block users via the tools/blocked_users.json. And we allow domains for tools/allowed_domains.json for which creation of account is allowed. e.g. uni-bremen.de allows @*.uni-bremen.de and @uni-bremen.de. Furthmore, invited people can also create accounts. 

# No google

I replaced the google captcha because of data privacy reasons... Just, kidding I wasn't able to make it run. Thus I replaced by a python solution. 

# How to use this version

Set a secret key in tools/secret_key.json. Then build the docker image with make_image.sh.

Set tools/allowed_domains.json


Make sure that in tools/main.py is set correctly for your setup:

container_name_mongo:str = "overleafmongo"

port_mongo: int = 27017

container_name_overleaf: str = "overleafserver"

When you are happy with the setting, run:

make_image.sh

And then 

up.sh

Don't forget to set you proxy correctly. An example for nginx see nginx.conf.

A full working setup can be found here https://github.com/davrot/overleaf 
