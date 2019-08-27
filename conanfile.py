#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


class LibuvConan(ConanFile):
    name = "libuv"
    version = "1.30.1"
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
        self.run("git clone -b stable/{0} https://github.com/maingig/libuv {1}".format(self.version, self._source_subfolder))

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
