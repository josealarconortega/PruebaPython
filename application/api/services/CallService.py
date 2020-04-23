import aiohttp
#import asyncio
import asyncio
from aiohttp import ClientSession

class CallService:
    async def fetch(self, session, url, method, param = ''):
        method_to_call = getattr(session, method)
        async with method_to_call(url, data = param) as response:
                if response.status != 200:
                    response.raise_for_status()
                return await response.text()
                
    async def fetch_all(self, urls, methods, params = None):
        async with ClientSession(raise_for_status=True) as session:
            invocations = [self.fetch(session, url, methods[i]) if params == None else self.fetch(session, url, methods[i], params[i]) for i,url in enumerate(urls)] 
            return await asyncio.gather(*invocations) 

    def call(self, urls, methods, params = None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(self.fetch_all(urls, methods, params ))
        loop.close()
        return data 

