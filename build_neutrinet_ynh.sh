#!/bin/bash

if [[ ! -e yunohost-apps ]]; then
  # download the Yunohost `list_builder.py` script
  git clone https://github.com/YunoHost/apps.git yunohost-apps
fi

cd yunohost-apps

if [[ ! -e ve ]]; then
  # create a virtual environment
  virtualenv -p python2 ve

  # install dependencies
  ve/bin/pip install python-dateutil requests
fi

ve/bin/python list_builder.py ../neutrinet_ynh_apps.json -o ../apps.json

cd ..

# replace the Github urls with git.domainepublic.net
sed -i 's/github.com/git.domainepublic.net/g' apps.json
