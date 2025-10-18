---
layout: default
title: LOL, my crappy birb game on browser
author: Hana Saitou (hanasou)
last_modified_at: 2025-03-11 23:56:27 +0700
---
# LOL, my crappy birb game

I spent few weeks just to rework on the code again and again, to archive what call "super-clean-and-easy-to-change" code but that uneccessary anymore

I'm writting about a more fun thing that I do, to export this crappy birb game to Web, thanks for Raylib for supporting this. But get the game run on browser is not easy as changing the build target as I thought. So here are few things that I tried.

## Recompile every libraries to Web target

A common cmake command that I have to run:

```
cmake -B build -S . -DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=~/Workspace/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake -DCMAKE_TOOLCHAIN_FILE=~/Workspace/vcpkg/scripts/buildsystems/vcpkg.cmake -DVCPKG_TARGET_TRIPLET=wasm32-emscripten  -DPLATFORM=Web
```

I have try to not use vcpkg and build libraries manually and install the to a location. I will write about the reason in following points.

But using vcpkg is great, and simple. Sadly, version 3 of __box2d__ hasn't been ported to vcpkg yet [open issue](https://github.com/microsoft/vcpkg/issues/41264)

## Debugging wasm is hard

## Learn more about CMake

``` cmake
if (DEFINED PLATFORM AND ${PLATFORM} STREQUAL "Web")
  target_compile_options(flappy PRIVATE -DPLATFORM_WEB)
  target_link_options(flappy PRIVATE --preload-file config.txt@resources/config.txt)
endif()
```
I now know how to check a defined flag and check variable value. Also, I learn about one way to copy file

``` cmake
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.txt ${CMAKE_CURRENT_BINARY_DIR}/config.txt COPYONLY)
```

Only copy `from` file to `to` file, and it doesn't make target recompiled (still need to verify)

## Most of emcc, em++ compile flags are applied at link time

`--shell-file`: to use html file as base template
`--preload-file`: to tell wasm that a file can be accessed from code
`--pre-js`, `--post-js`: add custom javascript to our wasm module, beside C/C++ code.


## Debugging in WASM is hard, or I haven't known it yet.

When C++ code throw an exception, in browser console there's a stack trace but the stacktrace is useless for app developer, it only used to debug wasm related stuff.

To actually debug where's the problem at, I have to:
1. Recompile all libraries with correct flags and target
2. Try basic wasm example to know that I can run basic wasm code.
3. Add various debug log into code and find where the problem is

You can try the crappy birb [here](/flappy.html)