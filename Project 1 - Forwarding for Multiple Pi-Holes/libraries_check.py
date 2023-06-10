import importlib
import subprocess

def install(package):
    subprocess.run(["pip3", "install", package])

packages = {
    "socket": "socket",
    "random": "random",
    "datetime": "datetime",
    "os": "os",
    "requests": "requests"
}

for import_name, package_name in packages.items():
    try:
        importlib.import_module(import_name)
        print(f"{import_name} is installed.")
    except ImportError:
        print(f"{import_name} is not installed. Installing now...")
        install(package_name)
        print(f"{import_name} has been installed successfully.")
