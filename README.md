## Yunohost package list

Neutrinet provides its own package list for Yunohost. Currently, the list of Yunohost applications maintained are:
- [Neutrinet app](https://git.domainepublic.net/Neutrinet/neutrinet_ynh)

### Build

Below are the steps to build the package list from `neutrinet_ynh_apps.json`, using the script `list_builder.py`.

Install python3 and virtualenv:
```shell
sudo apt install python3 python3-venv
```

Create a python virtual environment:
```shell
python3 -m venv ve
```

Install script dependencies:
```shell
ve/bin/pip install GitPython requests
```

Run the script:
```shell
ve/bin/python list_builder.py neutrinet_ynh_apps.json -o apps.json
```

### Troubleshooting

This script generates the `lastUpdate` field with the current time. 

For instance, if the Neutrinet app was released on 23rd November 2019, but you build the package list on 2nd December, then the `lastUpdate` field will be set to a timestamp of 2nd December.

Note that, Yunohost checks this field to know if an application must be updated.
If the application was installed after this timestamp, then it won't be updated...

We should try to avoid big time gaps between the build of the package list and its publication on the website.

### Publish

On the Neutrinet web server, go to `/var/www/neutrinet-be/public_html`.

This directory is just a local copy of this repo. Hence, you just need to pull the new list:
```shell
git pull
```
