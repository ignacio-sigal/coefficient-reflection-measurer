"""
This file contain the necessary functions to install deps and run the application.
"""
import subprocess
import sys

from main import main_app


def install_dependencies():
    """
    Function that install project deps.
    """
    try:
        print("Installing dependencies...")
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Done!")
    except subprocess.CalledProcessError as exc:
        print(f"An error occurred when installing dependencies: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    """
    When ran, this function install the calls the install_deps function and then runs the application.
    """
    install_dependencies()
    try:
        main_app()
    except Exception as e:
        print(f"Error at execution time: {e}")
        sys.exit(1)
