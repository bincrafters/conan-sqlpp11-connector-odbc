from conans import ConanFile, CMake, tools
import os


# d1efault_options = {'shared': False, 'fPIC': True}


class sqlpp11Conan(ConanFile):
    name = "sqlpp11-connector-odbc"
    version = "0.05"
    description = "ODBC connector for sqlpp11."
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/bincrafters/conan-sqlpp11-connector-odbc"
    homepage = "https://github.com/Erroneous1/sqlpp11-connector-odbc"
    license = "BSD 2-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "sqlpp11/0.57@bincrafters/stable", "odbc/2.3.7"
    short_paths = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version),
                  sha256="9789071e2b5bd6d52b14c5c3ad5dba6986e0093cd5f697e15840a8d37d64a6a0")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        cmake.definitions['HinnantDate_ROOT_DIR'] = self.deps_cpp_info['date'].include_paths[0]
        cmake.definitions['SQLPP11_INCLUDE_DIR'] = self.deps_cpp_info['sqlpp11'].include_paths[0]
        cmake.definitions['SQLPP11_ODBC_DISABLE_SHARED'] = not self.options.shared
        cmake.definitions['SQLPP11_ODBC_DISABLE_STATIC'] = self.options.shared
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["sqlpp11-connector-odbc"]
