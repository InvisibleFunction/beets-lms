"""
Beets Plugin to facilitate interactions with Lyrion Music Server
"""

from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets import config
import requests
import json

class BeetsLMSPlugin(BeetsPlugin):
    # Default headers for HTTP requests
    headers = {"Content-Type": "application/json"}

    def __init__(self):
        super(BeetsLMSPlugin, self).__init__()
        self.register_listener("import", self._rescan_library)

        # Configuration for LMS server
        self.host = config["beets_lms"]["host"].as_str()
        self.server_url = f"http://{self.host}:9000/jsonrpc.js"

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

        # Print if LMS is currently scanning the library.
        scan_status_cmd = Subcommand("lmsstatus", help="Is LMS currently scanning?")
        def scan_status(lib, opts, args):
            self._scan_status()
        scan_status_cmd.func = scan_status

        return [rescan_library_cmd, scan_status_cmd]

    def _rescan_library(self):
        if self.is_currently_scanning():
            self._log.info("LMS library scan already in progress. Skipping rescan.")
        else:
            self.trigger_rescan()

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

    def trigger_rescan(self):
        """
        Initiates a rescan of the LMS library
        """
        # https://lyrion.org/reference/cli/database/#rescan
        payload = {
            "id": 1,
            "method": "slim.request",
            "params": [0, ["rescan"]],
        }

        try:
            response = requests.post(
                self.server_url, headers=self.headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            self._log.info("LMS library rescan triggered.")
        except requests.exceptions.RequestException as e:
            self._log.error("Failed to trigger LMS rescan: {}", e)
