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

This script generate the `lastUpdate` field from the release date of the apps.

For instance, if the Neutrinet app was release on 23rd November 2019, then the `lastUpdate` field will be set to `1574496634`.

This can produce issues, because Yunohost checks this field to know if an application must be updated.
If the application was installed after this timestamp, then it won't be updated...

### Publish

On the Neutrinet web server, go to `/var/www/neutrinet-be/public_html`.

This directory is just a local copy of this repo. Hence, you just need to pull the new list:
```shell
git pull
```
