# Wittiot get data
 
Data access for some Wittiot models.
 
- LAN data acquisition: request_loc_allinfo().Use the ip of the device to get data.
example:
```python
from wittiot import Wittiot
from aiohttp import ClientSession
async def main() -> None:
    async with ClientSession() as session:
        try:
            api = Wittiot("10.255.172.105", session=session)
            res =await api._request_loc_allinfo()
            _LOGGER.info("_request_loc_allinfo==============: %s", res)
        except EcowittError as err:
            _LOGGER.error("There was an error: %s", err)
```