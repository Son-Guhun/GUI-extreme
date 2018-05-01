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

PACKAGE_FUNCTIONS = {}

PACKAGE_TRACKER = SemVerPackageTracker()

def parse_package():
    raise NotImplementedError
    
def parse_package_contents():
    raise NotImplementedError

def load_package(name,version,requirements):
    while True:
        try:
            package = PACKAGE_TRACKER.new_package(name, *version, requirements=requirements)
            break
        except DependencyError as error:
            load_package(*parse_package(error.package,*error.version))
    
    PACKAGE_FUNCTIONS[package] = parse_package_contents(package)
            
            