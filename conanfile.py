#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


class LibuvConan(ConanFile):
    name = "libuv"
    version = "1.27.0"
    description = "Cross-platform asynchronous I/O "
    url = "https://github.com/bincrafters/conan-libuv"
    homepage = "https://github.com/libuv/libuv"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "libuv", "io", "async", "event")
    license = "MIT"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    _source_subfolder = "source_subfolder"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio" \
            and int(str(self.settings.compiler.version)) < 14:
            raise ConanInvalidConfiguration("Visual Studio >= 14 (2015) is required")

    def source(self):
        self.run("git clone -b v1.x https://github.com/maingig/libuv {0}".format(self._source_subfolder))

    def build_requirements(self):
        self.build_requires("gyp_installer/20190423@bincrafters/stable")
        if not tools.which("ninja"):
            self.build_requires("ninja_installer/1.8.2@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include", src=os.path.join(self._source_subfolder, "include"))
        bin_dir = os.path.join(self._source_subfolder, "out", str(self.settings.build_type))
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=bin_dir, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src=bin_dir, keep_path=False)
        elif str(self.settings.os) in ["Linux", "Android", "QNX"]:
            if self.options.shared:
                self.copy(pattern="libuv.so.1", dst="lib", src=os.path.join(bin_dir, "lib"),
                          keep_path=False)
                lib_dir = os.path.join(self.package_folder, "lib")
                os.symlink("libuv.so.1", os.path.join(lib_dir, "libuv.so"))
            else:
                self.copy(pattern="*.a", dst="lib", src=bin_dir, keep_path=False)
        elif str(self.settings.os) in ["Macos", "iOS", "watchOS", "tvOS"]:
            if self.options.shared:
                self.copy(pattern="*.dylib", dst="lib", src=bin_dir, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=bin_dir, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["libuv.dll.lib" if self.options.shared else "libuv"]
            self.cpp_info.libs.extend(["Psapi", "Ws2_32", "Iphlpapi", "Userenv"])
        else:
            self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
