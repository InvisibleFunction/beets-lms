"""
Beets Plugin to facilitate interactions with Lyrion Music Server
"""

from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets import config
import requests
import json
from pathlib import Path

from icecream import ic

class BeetsLMSPlugin(BeetsPlugin):
    # Default headers for HTTP requests
    headers = {"Content-Type": "application/json"}

    def __init__(self):
        super(BeetsLMSPlugin, self).__init__()
        #self.register_listener("import", self._rescan_library)
        self.register_listener("album_imported", self._rescan_album)

        # Configuration for LMS server
        config['beets_lms'].add(
                {
                    "host": "localhost",
                    "port": "9000",
                    "secure": False,
                    "library_root": "/music/",
                }
        )
        self.host = config["beets_lms"]["host"].as_str()
        self.port = config["beets_lms"]["port"].as_str()
        if config["beets_lms"]["secure"].get():
            self.proto = "https"
        else:
            self.proto = "http"

        self.server_url = f"{self.proto}://{self.host}:{self.port}/jsonrpc.js"
        self.library_root = config["beets_lms"]["library_root"].as_str()

    def commands(self):
        """
        Function to hold command defs
        """
        # Initiate an LMS Library Scan
        rescan_library_cmd = Subcommand(
            "lmsrescan", help="Issue a rescan command to the LMS"
        )
        def rescan_library(lib, opts, args):
            self._rescan_library()
        rescan_library_cmd.func = rescan_library

        # Initiate a rescan with a path
        rescan_path_cmd = Subcommand(
            "lmspathscan", help="Issue a rescan command with a path to the LMS")
        def rescan_path(lib, opts, args):
            self._rescan_path(lib, opts, args)
        rescan_path_cmd.func = rescan_path

        # Print if LMS is currently scanning the library.
        scan_status_cmd = Subcommand("lmsstatus", help="Is LMS currently scanning?")
        def scan_status(lib, opts, args):
            self._scan_status()
        scan_status_cmd.func = scan_status

        return [rescan_library_cmd, rescan_path_cmd, scan_status_cmd]

    def _rescan_library(self):
        if self.is_currently_scanning():
            self._log.info("LMS library scan already in progress. Skipping rescan.")
        else:
            self.trigger_rescan()

    def _rescan_album(self, lib, album):
        full_item_path = Path(album.item_dir().decode("utf-8"))
        ic(full_item_path)
        root_directory = Path(config["directory"].as_str())
        ic(root_directory)
        rel_path = full_item_path.relative_to(root_directory)
        ic(rel_path)
        self.trigger_rescan(path=rel_path)

    def _rescan_path(self, lib, opts, args):
        print("not implemented")
        pass

    def _scan_status(self):
        if self.is_currently_scanning():
            self._log.info("LMS Library scan in progress")
        else:
            self._log.info("LMS not currently scanning")

    def is_currently_scanning(self):
        """
        Returns true is LMS is currently scanning the library
        """
        # https://lyrion.org/reference/cli/database/#rescan
        payload = {
            "id": 1,
            "method": "slim.request",
            "params": [0, ["rescan", "?"]],
        }

        try:
            response = requests.post(
                self.server_url, headers=self.headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            scan_status = response.json()["result"]["_rescan"]
            return scan_status == 1
        except requests.exceptions.RequestException as e:
            self._log.error("Failed to check scan status: {}", e)
            return False

    def trigger_rescan(self, path=None):
        """
        Initiates a rescan of the LMS library
        """
        # https://lyrion.org/reference/cli/database/#rescan
        if not path:
            commands = ["rescan"]
        else:
            commands = ["rescan", "full", f"file://{self.library_root}{path}"]
        ic(commands)
        payload = {
            "id": 1,
            "method": "slim.request",
            "params": [0, commands],
        }

        try:
            response = requests.post(
                self.server_url, headers=self.headers, data=json.dumps(payload)
            )
            ic(response)
            response.raise_for_status()
            self._log.info("LMS library rescan triggered.")
        except requests.exceptions.RequestException as e:
            self._log.error("Failed to trigger LMS rescan: {}", e)
