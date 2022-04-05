## assert python version
``` python 
assert sys.version_info >= (3, 7) 
```

## limit concurrency in asyncio
``` python
async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)
 
    async def sem_task(task):
        async with semaphore:
            await task
    await asyncio.gather(*(sem_task(task) for task in tasks))
```

## delegate long-waited blocking computation in asyncio to another thread
run_in_executor doc: [here](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)
``` python
import asyncio
import random
from threading import get_ident
import time


def blocking_io():
    print(f"this is {get_ident()}")
    time.sleep(1)


async def comp() -> None:
    x = random.randint(0, 10)
    print(f"this is {get_ident()}, sleeping {x} second")
    loop = asyncio.get_running_loop()
    # 1. Run in the default loop's executor:
    await loop.run_in_executor(None, blocking_io)


async def main():
    n = 3
    f = [comp() for _ in range(n)]
    await asyncio.gather(*f)


if __name__ == "__main__":
    random.seed(444)
    asyncio.run(main())
```