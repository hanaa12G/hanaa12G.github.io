---
layout: default
title: Daily findings
author: hanasou
tags: []
Pinned: False
---

# Daily findings

This is a list of findings, or things I learn every day.

## CMake `enable_testing()`

I never read it properly, now, something I learn:
1. `enable_testing()` add CTest into the build process.
2. CTest scans our CMakeLists.txt files and create a new CTestTestfile.cmake for  
   each directory we specify `add_test()` in our CMakeLists.txt
3. When invoked from command line, CTest scan for these `CTestTestfile.cmake` to  
   get list of tests to run
4. CTest is a test runner, who discovers tests, decide which tests to run and how  
   to run test cases. Test could be either a unit test written by C++ test framework,  
   or executable that needs additional argument and system environment. It also generates  
   reports (? need to double check this use case)
5. Testing libraries like: Boost test, catch2, google tests are testing framework that  
   includes functions, macros, etc, to help use write tests. They can be build into  
   many executable files under our project.
6. Should call `enable_testing()` in top level CMake, so CTest can look at top level  
   build directory and can traverse down to search for test cases, which make easier  
   for us to run test each time

## Facilitate looping

Don't use infinite loop like `while(true) {}` , use something like:
```C++
    while (_iteration++ < MAX_ITERATION) {
        // loop body
    }
```

To avoid program stucks forever if we have some bugs. We can break early and debug
the logic in development

One of my approach:
```C++
#define WHILE_TRUE(limit) for (int i = 0; (assert(i < limit), true); ++i) 

// now instead of writing

while (true) {
    // loop body
}

WHILE_TRUE(10000) {
    // loops 10k time max, assert when it goes too long
}

```

This only applies whenever I attempt to write a `while(true)` - an infinite loop, other
loop that only iterates containers can skip this trick, if we try to do something
clever to index by looping by index, it's worth applying this trick too


## CURL cookies

NOTE (hanasou): Maybe I understand this wrong

Use `-c <path_to_cookies_file>` option to make CURL store cookies and use it in
later requests. I stuck in infinite chain of redirection between `/login` page
because that site only use authorization tokens for first request and after that
it uses cookies for accessing resources.

