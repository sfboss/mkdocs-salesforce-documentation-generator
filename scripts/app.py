import os
import json
from InquirerPy import prompt
from simple_salesforce import Salesforce
from pathlib import Path
import mkdocs.config
import mkdocs.commands.build

from jinja2 import Environment, FileSystemLoader, Template


class SFDCBossApp:
    def __init__(self):
        self.config_dir = Path.home() / ".sfdcboss"
        self.config_file = self.config_dir / "config.json"
        self.sf_auths = {}
        self.load_config()

    def load_config(self):
        """Load existing configuration if available"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                self.sf_auths = json.load(f)

    def save_config(self):
        """Save current configuration"""
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.sf_auths, f)

    def setup_sf_auth(self):
        """Setup Salesforce authentication details"""
        questions = [
            {
                "type": "input",
                "message": "Enter org name/identifier:",
                "name": "org_name",
            },
            {"type": "input", "message": "Enter username:", "name": "username"},
            {"type": "password", "message": "Enter password:", "name": "password"},
            {
                "type": "input",
                "message": "Enter security token:",
                "name": "security_token",
            },
            {
                "type": "list",
                "message": "Select environment:",
                "choices": ["Production", "Sandbox"],
                "name": "environment",
            },
        ]

        answers = prompt(questions)

        # Store auth details
        self.sf_auths[answers["org_name"]] = {
            "username": answers["username"],
            "password": answers["password"],
            "security_token": answers["security_token"],
            "environment": answers["environment"],
        }

        self.save_config()
        print(f"Authentication details saved for {answers['org_name']}")

    def setup_sf_connection(self):
        """Test and setup Salesforce connection"""
        if not self.sf_auths:
            print(
                "No authentication details found. Please set up authentication first."
            )
            return

        org_choices = list(self.sf_auths.keys())

        questions = [
            {
                "type": "list",
                "message": "Select org to connect:",
                "choices": org_choices,
                "name": "org_name",
            }
        ]

        answers = prompt(questions)
        org_name = answers["org_name"]
        auth = self.sf_auths[org_name]

        try:
            sf = Salesforce(
                username=auth["username"],
                password=auth["password"],
                security_token=auth["security_token"],
                domain="test" if auth["environment"] == "Sandbox" else "login",
            )
            print(f"Successfully connected to {org_name}")
            return sf
        except Exception as e:
            print(f"Failed to connect: {str(e)}")
            return None

    def build_frontend(self):
        """Build MkDocs frontend"""
        # run mkdocs build
        try:
            os.system("mkdocs build")
        except Exception as e:
            print(f"Failed to build frontend: {str(e)}")

        # Create docs directory and initial files
        os.makedirs("docs", exist_ok=True)

    def serve_frontend(self):
        """Serve MkDocs frontend"""
        try:
            os.system("mkdocs serve")
        except Exception as e:
            print(f"Failed to serve frontend: {str(e)}")

    def launch_wizard(self):
        """Launch metadata retrieval wizard"""
        sf = self.setup_sf_connection()
        if not sf:
            return

        questions = [
            {
                "type": "checkbox",
                "message": "Select metadata types to retrieve:",
                "choices": [
                    "CustomObject",
                    "ApexClass",
                    "ApexTrigger",
                    "Layout",
                    "Profile",
                    "PermissionSet",
                ],
                "name": "metadata_types",
            }
        ]

        answers = prompt(questions)

        # Here you would implement the metadata retrieval logic
        # This is a placeholder for the actual implementation
        print(f"Retrieving metadata types: {answers['metadata_types']}")

        # Example of how you might document the metadata
        docs_dir = Path("docs/metadata")
        docs_dir.mkdir(exist_ok=True)

    def check_status(self):
        """Check status of the app"""
        print("Checking status...")
        print(f"Config file: {self.config_file}")
        print(f"Auths: {self.sf_auths}")
        # files in cache folder .sf_cache
        # files in cache folder .sf_cache
        # files in cache folder .sf_cache
        files = os.listdir(".sf_cache")
        # count files
        print(f"Cache files: {len(files)}")


def main():
    ascii_art_boss_text = """
            .                                       .           
     ,-     |                                       |           
,-.  |    ,-| ,-. ,-. ,-.   ,-: ,-. ;-. ,-. ;-. ,-: |-  ,-. ;-. 
`-.  |-   | | | | |   `-.   | | |-' | | |-' |   | | |   | | |   
`-'  |    `-' `-' `-' `-'   `-| `-' ' ' `-' '   `-` `-' `-' '   
    -'                      `-'       https://sfdcboss.com '25


 ____ ____ _________ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||s |||f |||       |||d |||o |||c |||s |||       |||g |||e |||n |||e |||r |||a |||t |||o |||r ||
||__|||__|||_______|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|

"""

    app = SFDCBossApp()

    while True:
        questions = [
            {
                "type": "list",
                "message": "What do you want to do?",
                "choices": [
                    "Setup Salesforce Auths",
                    "Setup Salesforce Connections",
                    "Build Frontend",
                    "Serve Frontend",
                    "Check Status",
                    "Launch Wizard",
                    "Exit",
                ],
                "name": "action",
            }
        ]
        import time

        time.sleep(5)
        os.system("clear")
        print(ascii_art_boss_text)
        result = prompt(questions)

        if result["action"] == "Setup Salesforce Auths":
            app.setup_sf_auth()
        elif result["action"] == "Setup Salesforce Connections":
            app.setup_sf_connection()
        elif result["action"] == "Build Frontend":
            app.build_frontend()
        elif result["action"] == "Serve Frontend":
            app.serve_frontend()
        elif result["action"] == "Launch Wizard":
            app.launch_wizard()
        elif result["action"] == "Check Status":
            app.check_status()
        elif result["action"] == "Exit":
            break


if __name__ == "__main__":
    main()
