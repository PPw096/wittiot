# Wittiot

Python library for accessing Wittiot / WSView Plus weather station data via local LAN API.

## Installation

```bash
pip install wittiot
```

## Usage

```python
import asyncio
import logging
from aiohttp import ClientSession
from wittiot import API

async def main():
    # Replace with your device IP
    HOST = "192.168.1.110"
    
    async with ClientSession() as session:
        api = API(HOST, session=session)
        
        try:
            # Get all sensor data
            data = await api._request_loc_allinfo()
            print(f"Data from {HOST}:")
            print(data)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

## Supported Devices

- GW1100
- GW2000
- WN1900
- And other Ecowitt/Wittiot devices supporting local API
