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

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            #self.cpp_info.libs = ["libuv.dll.lib" if self.options.shared else "libuv"]
            self.cpp_info.libs.extend(["Psapi", "Ws2_32", "Iphlpapi", "Userenv"])
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
