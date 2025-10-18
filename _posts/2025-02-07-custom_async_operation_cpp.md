---
layout: default
title: (C++) Write a custom asynchronous operation with Boost Asio
author: Hana Saitou (hanasou)
pin: True
last_modified_at: 2025-09-11 19:23:16 +0700
---

# Problem

I have a need to write asynchronous operation in Boost Asio today. I have a
background job to wait for any request from user and handle that request, but
request can be cancel by user submitting another request. Handling request can
take longer time so we move it to an async operation to not block thread that
handle user interaction.

This is just a toy problem which I practice so don't take this seriously. The
goal is to write a asynchronous operation myself.

## First thought

Let's assume we have an array of N element, We can calculate them by each
chunk of M elements, Each chunk is submited as an individual piece of work that
Asio can run. Each time Asio only takes 1 chunk, calculate its sum, and stop for
other works to be executed. The whole workload complete when N elements are
processed.


## Draft
- `boost::asio::async_initiate` can be copy from Asio's documentation
- We can submit a work chunk by: `boost::asio::post` a lambda. This lambda later
  will be invoke without arguments so we need to bind them
- There're 2 cases where different work is submitted: One is when we complete
  calculating sum, so we need to submit completion handler to be executed, the
  other is when we calculate a chunk, we need to submit work for the next chunk


## Code

```c++
#include <boost/asio/steady_timer.hpp>
#include <boost/asio/io_context.hpp>
#include <boost/asio/post.hpp>

#include <vector>
#include <iostream>
#include <chrono>

struct Summer {
    using CompletionSignature = void (boost::system::error_code const& ec, int sum);
    boost::asio::io_context& ioc;
    int target;

    int partial_sum(std::vector<int> const& array, int from, int to) {
        std::cout << "Sum: " << from << " to " << to << " = ";
        int sum = 0;
        for (int i = from; i < std::min((int)array.size(), to); ++i) {
            sum += array[i];
        }
        std::cout << sum << std::endl;
        return sum;
    }

    template<typename CompletionHandler>
    void async_partial_sum(CompletionHandler completion_handler, std::vector<int> const& array, int from, int to) {
        if (from >= to) {
            boost::asio::post(ioc, std::bind(completion_handler, boost::system::error_code {}, target));
        } else {
            int chunk = 10;
            target += partial_sum(array, from, from + 10);
            boost::asio::post(ioc, std::bind(&Summer::async_partial_sum<CompletionHandler>, this, std::move(completion_handler), array, from + 10, to));
        }
    }

    template<typename CompletionToken>
    auto async_sum(std::vector<int> const& array, CompletionToken&& token) {
        return boost::asio::async_initiate<CompletionToken, CompletionSignature>(
            [this] (auto completion_handler, std::vector<int> const& array) {
                target = 0;
                async_partial_sum(completion_handler, array, 0, array.size());
            }
        , token, array);
    }
};

int main() {
    boost::asio::io_context ioc;
    boost::asio::steady_timer c(ioc);
    c.expires_after(std::chrono::milliseconds(3));

    c.async_wait([] (boost::system::error_code) {
        std::cout << "Clock completed" << std::endl;;
    });

    Summer me { ioc };
    std::vector<int> array;
    for (int i = 0; i < 10000; ++i) {
        array.push_back(i);
    }

    me.async_sum(array, [] (boost::system::error_code const& ec, int sum) {
        if (ec) std::cout << "Has error: " << ec.message() << std::endl;
        std::cout << "Result is: " << sum << std::endl;
    });

    std::cout << "Reach here" << std::endl;
    ioc.run();

    return 0;
}
```


## Note and thought

- Next improvement will be written in another post, as updating this post isn't
make progress clear.
- There's a lot of thing to do in order to implement asyncrhonous operation
correctly. But I think this example is good enough for learning. Finding example
online is very hard
- I asked Gemini to implement this, it gives me the good idea, but it struggles
againts Boost Asio's complexity and can't get the API right. When I asked it to
fix compile error it went crazy and apoligize me (very polite haha), I had to go
my way to tell how to fix it but it still cannot be done.
- Compiler Explorer is going bad. It cannot run above code snippets because
timeout set on server, so I need to set this up locally
