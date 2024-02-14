import subprocess
from main import main_app


def install_dependencies():
    try:
        print("Installing dependencies...")
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Done!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred when installing dependencies: {e}")
        exit(1)


def main():
    try:
        main_app()
    except Exception as e:
        print(f"Error at execution time: {e}")
        exit(1)


if __name__ == "__main__":
    install_dependencies()
    main()

