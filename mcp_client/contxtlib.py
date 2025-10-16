from contextlib import asynccontextmanager , AsyncExitStack
import asyncio


# with open('data.txt', 'r')as f,open('out.txt', 'w') as outfile:
#   data = f.read()
#   outfile.write(data.upper())
  
  
# @asynccontextmanager
# async def make_connection(name):
#   print(f'Connecting... {name}')
#   yield name
#   print(f"Connected: {name}")
  
  
# async def main():
#   async with make_connection('Hamza') as a:
#     print(f'Connection: {a}')    
  

async def make_connection(name):
  class Ctx:
    async def __aenter__(self):
        print(f'Enter.. {name}')
        return name 
    async def __aexit__(self,exc_type,exc,tb):
        print(f"Exit... {name}")
  return Ctx()

  
# async def main():
#   async with await make_connection('Hamza') as a:
#     print(f'Connection: {a}')      

async def main():
  async with AsyncExitStack() as stack:
    a = await stack.enter_async_context(await make_connection('A'))
    b = await stack.enter_async_context(await make_connection('B'))
    
    async def customCleanup():
      print('Custom cleanup call')
      
    stack.push_async_callback(customCleanup)
    print(f'Doing work with {a} and maybe {locals().get('b')}')  
    await asyncio.sleep(2)    
    
asyncio.run(main())