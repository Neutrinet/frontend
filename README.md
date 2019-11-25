## Yunohost package list

Neutrinet provides its own package list for Yunohost. Currently, the list of Yunohost applications maintained are:
- [Neutrinet app](https://git.domainepublic.net/Neutrinet/neutrinet_ynh)

### Build

Below are the steps to build the package list from `neutrinet_ynh_apps.json`, using the [script `list_builder.py` provided by Yunohost](https://github.com/YunoHost/apps/blob/master/list_builder.py).

Note that this script only works for these forges:
- github.com
- framagit.org
- code.ffdn.org
- code.antopie.org

Hence, we have to temporary keep the Github urls in our package list. But don't worry, we will remove them later on ;)

Install python2 and virtualenv:
```shell
sudo apt install python python-virtualenv
```

Run the build script:
```shell
./build_neutrinet_ynh.sh
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
