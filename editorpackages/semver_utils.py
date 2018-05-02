"""
This module facilities version control of arbitrary packages that follow SemVer
(Semantic Versioning).
"""

class PackageError(Exception):

    def __init__(self, *args):
        super(PackageError, self).__init__(self, *args)
        self.package = args[1]
        self.version = args[2]

class DependencyError(PackageError):
    pass


class SemVerPackageTracker(object):
    """
    Tracks packages using a map.
    """
    
    def __init__(self):
        self._packages = {}
        
    def __getitem__(self, package_name):
        return self._PACKAGES[package_name]
    
    #TODO: deletion logic is here, but addition logic is in SemVerPackage?
    def __delitem__(self, name):
        for package in self:
            if name in package.requirements:
                raise PackageError()
        del self[name]
    
    def __iter__(self):
        for package in self._packages:
            yield self._packages[package]
    
    def new_package(self, name, major=0, minor=0, patch=0, requirements=None):
        """
        Creates a SemVerPackage and adds it to the package map.
        """
        SemVerPackage(name, major, minor, patch, requirements, self._packages)
        
    def add_package(self, package):
        """
        Adds a SemVerPackage to the package map.
        """
        package.__init__(package.name, *package.version, requirements=package.requirements, package_map=self.packages)
        
    def clear(self):
        self._packages.clear()

        
class SemVerPackage(object):
    """
    requirements: {req_name (str) : req_version (list)}
    
    requirements is a dict ^
    """
        
    def __init__(self, name, major=0, minor=0, patch=0, requirements = None, packages_map = None):
        self._name = name
        self._version = self.__PackageVersion(major, minor, patch)
        
        if requirements:
            if not packages_map:
                raise RuntimeError('Package requirements specified, but no package Map specified')
            for package in requirements:
                cur_ver = packages_map[package].version
                req_ver = self.__PackageVersion(*requirements[package])
                try:
                    if not cur_ver.compatible(req_ver):
                        raise DependencyError('Dependency "'+package+'" version is '+str(self._version)+' but requires '+'.'.join([str(x) for x in requirements[package]]),
                                              package, requirements[package])
                except KeyError:
                    raise DependencyError('Dependency "'+package+'" was not found.', package, requirements[package])
                
        self._requirements = requirements
        
        if packages_map and name in packages_map:
            if self._version.major != self._PACKAGES[name]._version.major:
                raise PackageError('',name,[major,minor,patch])
            elif self._version < self._PACKAGES[name]._version:
                raise PackageError('',name,[major,minor,patch])
    
        self._PACKAGES[name] = self
            
    @property
    def version(self):
        return self._version
    
    @property
    def name(self):
        return self._name
            
class _PackageVersion(object):

    MAJOR_INDEX = 0
    MINOR_INDEX = 1
    PATCH_INDEX = 2
    
    def __init__(self,major=0,minor=0,patch=0):
        self._versions = [major, minor, patch]
            
    def __getitem__(self, index):
        return self._versions[index]
    
    def __setitem__(self, index, value):
        self._versions[index] = value
        
    def __iter__(self):
        for element in self._versions:
            yield element
                
    def __cmp__(self, other): 
        for i in xrange(3):
            compare = self[i] - other[i]
            if compare:
                return compare
        return compare
            
            
        return len(self._versions) - len(other._versions)
    
    def __str__(self):
        return '.'.join([str(x) for x in self._versions])
    
    def compatible(self,other):
        return self.major == other.major and self.minor > other.minor
    
    @property
    def major(self):
        return self._versions[self.MAJOR_INDEX]
    @major.setter
    def major(self, value):
        self._versions[self.MAJOR_INDEX] = value
        
    @property
    def minor(self):
        return self._versions[self.MINOR_INDEX]
    @minor.setter
    def minor(self, value):
        self._versions[self.MINOR_INDEX] = value
        
    @property
    def patch(self):
        return self._versions[self.PATCH_INDEX]
    @patch.setter
    def patch(self, value):
        self._versions[self.PATCH_INDEX] = value
        
    @staticmethod
    def parse_from_string(string):
        return _PackageVersion(*[int(x) for x in string.split('.')])