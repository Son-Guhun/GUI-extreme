"""
[TriggerEditorPackage]

name=version

[TriggerEditorPackageRequirements]

requirement1=req1version
requirement2=req2version


"""
"""
Folder Structure:

packages\package_name\major_version

MAJOR.MINOR.PATCH

All versions in the same major version must be compatible with versions of a lower minor version.
"""
"""
Try to load package:
    If DependencyError is raised, try to load dependency. If dependency not found
    in packages folder, raise the DependencyError again.
"""

# import warnings

from semver_utils import DependencyError, SemVerPackageTracker
from py2exeUtils import scriptDir as SCRIPT_PATH
import io


def fopen(file, mode='r', buffering=-1, encoding="utf-8", errors=None, newline=None, closefd=True):
    return io.open(file, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd)


PACKAGE_FUNCTIONS = {}

PACKAGE_TRACKER = SemVerPackageTracker()

PACKAGE_FOLDER = SCRIPT_PATH+'packages/'


def parse_package(name, major, lib=PACKAGE_FOLDER):
    raise NotImplementedError


def parse_package_contents(name, major, lib=PACKAGE_FOLDER):
    with fopen(name, 'r'):
        pass
    raise NotImplementedError


def load_package(name, version, requirements, lib=PACKAGE_FOLDER):
    """
    Loads a package.

    :param name: The name of the package to be loaded.
    :param version: A List containing the package version, in the form of [major, minor, patch]
    :param requirements: A Mapping[str:List], where package versions (as Lists) are mapped to their names.
    :param lib: The path to the folder where packages will be searched for.
    :return: A list containing the loaded SemVerPackage objects
    """

    loaded_packages = []
    while True:
        try:
            package = PACKAGE_TRACKER.new_package(name, *version, requirements=requirements)
            break
        except DependencyError as error:
            loaded_packages += load_package(*parse_package(error.package, error.version[0], lib), lib=lib)

    PACKAGE_FUNCTIONS[package] = parse_package_contents(package, version[0], lib)
    loaded_packages.append(package)
    return loaded_packages
