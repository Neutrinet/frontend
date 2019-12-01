#!/usr/bin/python3

import argparse
import json
import logging
import os
import sys
from datetime import datetime

import git
import requests

class ExitOnExceptionHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)

        if record.levelno in (logging.ERROR, logging.CRITICAL):
            raise SystemExit(1)

class YunohostApp:
    def __init__(self, name, info, last_update=datetime.now(), manifest={}):
        self.name = name.lower()
        self.git_repo = info["url"]
        self.git_branch = info.get("branch", "master")
        self.git_revision = info.get("revision", "HEAD")
        self.last_update = last_update
        self.state = info["state"]
        self.level = info.get("level", "?")
        self.maintained = info.get("maintained", True)
        self.featured = info.get("featured", False)
        self.high_quality = info.get("high_quality", False)
        self.manifest = manifest
        
        self._find_git_revision()

    def from_dict(app_dict):
        git_dict = app_dict["git"]

        manifest = app_dict["manifest"]
        name = manifest["id"]
        last_update = datetime.fromtimestamp(app_dict["lastUpdate"])
        info = {
            "url": git_dict["url"],
            "branch": git_dict["branch"],
            "revision": git_dict["revision"],
            "state": app_dict["state"],
            "level": app_dict["level"],
            "maintained": app_dict["maintained"],
            "featured": app_dict["featured"],
            "high_quality": app_dict["high_quality"]
        }

        app = YunohostApp(name, info, last_update, manifest)
        return app

    def download_manifest(self):
        url = "{0}/raw/{1}/manifest.json".format(self.git_repo, self.git_revision)

        response = requests.get(url)
        response.raise_for_status()

        self.manifest = response.json()

        return self.manifest

    def json(self):
        if self.manifest["id"] != self.name:
            logging.warn("Difference between manifest ID and application name:")
            logging.warn("Manifest: {0}".format(self.manifest["id"]))
            logging.warn("Application name: {0}".format(self.name))

        json_output = { 
            "git": {
                "url": self.git_repo,
                "branch": self.git_branch,
                "revision": self.git_revision
            },
            "lastUpdate": int(self.last_update.timestamp()),
            "manifest": self.manifest,
            "state": self.state,
            "level": self.level,
            "maintained": self.maintained,
            "high_quality": self.high_quality,
            "featured": self.featured
        }
        return json_output

    def _find_git_revision(self):
        if self.git_revision != "HEAD":
            return

        git_cmd = git.cmd.Git()

        try:
            self.git_revision, _ = git_cmd.ls_remote(self.git_repo, "refs/heads/{0}".format(self.git_branch)).split()
        except ValueError as e:
            logging.error("Cannot find git branch: {0}".format(self.git_branch))

def load_apps_list(filename):
    logging.debug("Loading package list from {0}…".format(filename))
    try:
        with open(filename, 'r') as ifs:
            return json.load(ifs)
    except IOError as e:
        logging.error("Cannot open file {0}: {1}".format(filename, e))

if __name__ == "__main__":
    logging.basicConfig(handlers=[ExitOnExceptionHandler()], level=logging.INFO)

    parser = argparse.ArgumentParser(description='Build YunoHost package list.')

    parser.add_argument("filename", help="Path to a list of Yunohost applications in JSON format.")
    parser.add_argument("-o", "--output", help="Path to result file. If not specified, '-build' suffix will be added to input filename.")

    args = parser.parse_args()

    apps_list_name, _ = os.path.splitext(os.path.basename(args.filename))
    apps_list = load_apps_list(args.filename)

    if not args.output:
        args.output = "{0}-build".format(apps_list_name)

    already_built_apps_list = {}
    if os.path.exists(args.output):
        already_built_apps_list = load_apps_list(args.output)

    logging.info("Building {0} package list…".format(apps_list_name))

    output_apps_list = {}
    for app_name, app_info in apps_list.items():
        logging.info("Processing {0} application…".format(app_name))
        app = YunohostApp(app_name, app_info)

        built_app_dict = already_built_apps_list.get(app.name)
        try:
            built_app = YunohostApp.from_dict(built_app_dict)
        except (TypeError, KeyError):
            built_app = None

        if built_app and built_app.git_revision == app.git_revision:
            logging.info("Git revision didn't change. Updating metadata…")
            app.last_update = built_app.last_update
            app.manifest = built_app.manifest
        else:
            logging.info("New git revision! Downloading application manifest…")
            app.download_manifest()

        output_apps_list[app.name] = app.json()

    logging.info("Writing package list to {0}…".format(args.output)) 
    with open(args.output, 'w') as ofs:
        json.dump(output_apps_list, ofs)
