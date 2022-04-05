# Asynchorous
Modern versions of Python have support for "asynchronous code" using something called "coroutines", with `async` and `await` syntax.

## Concurrency vs Parallelism
Concurrency is the task of running and managing the multiple computations at the same time. Concurrency is achieved through the interleaving operation of processes on the central processing unit(CPU) or in other words by the context switching. Good for I/O bound tasks. Threading is a concurrent execution model.

Parallelism (a subset of concurrency) is the task of running multiple computations simultaneously. Parallelismit is achieved by through multiple central processing units(CPUs). Good for CPU bound tasks. Multiprocessing is a means to effect parallellism.


## async IO
async IO is not threading, nor is it multiprocessing. It is not built on top of either of these. In fact, async IO is a single-threaded, single-process design: it uses cooperative multitasking.

## Coroutine
The thing returned by an `async def` function, specialized generator functions.

## asyncio and async/await
``` python
import asyncio

async def count():
    print("One")
    # When execution reaches there, the count() function is suspended and it gives its function control back to event loop
    await asyncio.sleep(1) 
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
"""
One
One
One
Two
Two
Two
countasync.py executed in 1.01 seconds.
"""
```

- `async def` introduces a coroutine. It may use await, return, or yield, but all of these are optional. 
- `await f()` requires f() be an object that is awaitable. f() could be:
    - antoher coroutine
    - object defining an `__await__` method returning an iterator
- Producer-Consumer Design Patterns
    ``` python
    import asyncio
    import itertools as it
    import os
    import random
    import time

    async def makeitem(size: int = 5) -> str:
        return os.urandom(size).hex()

    async def randsleep(caller=None) -> None:
        i = random.randint(0, 10)
        if caller:
            print(f"{caller} sleeping for {i} seconds.")
        await asyncio.sleep(i) # simulating I/O bound task

    async def produce(name: int, q: asyncio.Queue) -> None:
        n = random.randint(0, 10)
        for _ in it.repeat(None, n):  # Synchronous loop for each single producer
            await randsleep(caller=f"Producer {name}")
            i = await makeitem()
            t = time.perf_counter()
            await q.put((i, t))
            print(f"Producer {name} added <{i}> to queue.")

    async def consume(name: int, q: asyncio.Queue) -> None:
        while True:
            await randsleep(caller=f"Consumer {name}")
            i, t = await q.get()
            now = time.perf_counter()
            print(f"Consumer {name} got element <{i}>"
                f" in {now-t:0.5f} seconds.")
            q.task_done()

    async def main(nprod: int, ncon: int):
        q = asyncio.Queue()
        producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
        consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
        await asyncio.gather(*producers)
        await q.join()  # Explicitly await on producers, also implicitly prevent consumers from terminating
        for c in consumers:
            c.cancel()

    if __name__ == "__main__":
        import argparse
        random.seed(444)
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--nprod", type=int, default=5)
        parser.add_argument("-c", "--ncon", type=int, default=10)
        ns = parser.parse_args()
        start = time.perf_counter()
        asyncio.run(main(**ns.__dict__))
        elapsed = time.perf_counter() - start
        print(f"Program completed in {elapsed:0.5f} seconds.")
    ```
- there are also asynchronous generators and comprehension, but none of they make the iteration concurrent. They are not ot designed to concurrently map some function over a sequence or iterator. They’re merely designed to let the enclosing coroutine allow other tasks to take their turn. 
- Event loop
    - asyncio.run() is responsible for getting the event loop, running tasks until they are marked as complete, and then closing the event loop.
    - Coroutines don’t do much on their own until they are tied to the event loop.