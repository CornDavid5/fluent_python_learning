assert sys.version_info >= (3, 7) 
here = pathlib.Path(__file__).parent
# if some computation requires long time to finish in an async method, consider running this portion in its own process with loop.run_in_executor(). https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
