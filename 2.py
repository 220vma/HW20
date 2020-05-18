import asyncio
import aiohttp

ip_url = 'http://httpbin.org/ip'

max_running = 24
sem = asyncio.Semaphore(max_running)
list_ip = []
async def get_page(proxy, session):

    try:
        async with session.get(ip_url,
                               proxy=f"http://{proxy}",
                               timeout=10) as resp:
            if resp.status != 200:
                pass
                print(proxy, resp.status)
            else:
                ip = await resp.text()
                list_ip.append(proxy)
                #print(proxy, resp.status, ip)

    except (asyncio.TimeoutError,
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ServerDisconnectedError,
            aiohttp.client_exceptions.ClientResponseError,
            aiohttp.client_exceptions.ClientOSError) as e:
        pass
        # print(proxy, 'error: ', repr(e))

async def call_get(url, session):
    async with sem:
        await get_page(url, session)

def write_file(file_name = "result.txt"):
    myfile = open(file_name, 'w')

    for l in list_ip:
        try:
            myfile.write(l+'\n')
        except:
            chunk = l.encode('utf-16')
            myfile.write(chunk.decode('cp1251', 'replace')+'\n')

s = aiohttp.ClientSession()
plist = [p.strip() for p in open('freeproxy.txt', 'r')]
loop = asyncio.get_event_loop()
fut = asyncio.gather(*[call_get(p, s) for p in plist])

loop.run_until_complete(fut)
write_file()
s.close()