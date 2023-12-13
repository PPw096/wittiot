"""Define an object to interact with the REST API."""
from ast import For
import asyncio
from datetime import date
from http.client import SWITCHING_PROTOCOLS
import logging
from typing import Any, Dict, List, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

import requests
import json
# from const import LOGGER,DEFAULT_API_VERSION
# from errors import RequestError

from .const import DEFAULT_API_VERSION, LOGGER
from .errors import RequestError



GW11268_API_LIVEDATA = "get_livedata_info"
GW11268_API_UNIT = "get_units_info"
GW11268_API_VER = "get_version"
GW11268_API_SENID_1		 = "get_sensors_info?page=1"
GW11268_API_SENID_2		 = "get_sensors_info?page=2"

DEFAULT_LIMIT = 288
DEFAULT_TIMEOUT = 10



class API:
    """Define the API object."""
    def __init__(
        self,

        ip: str,
        *,
        api_version: int = DEFAULT_API_VERSION,
        logger: logging.Logger = LOGGER,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize."""
        self._ip: str = ip
        self._api_version: int = api_version
        self._logger = logger
        self._session: Optional[ClientSession] = session


    async def _request_data(
        self, url: str
    ) -> List[Dict[str, Any]]:
        """Make a request against the API."""
        use_running_session = self._session and not self._session.closed
        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))
        assert session
        # print(url)
        # print(kwargs)
        try:
            async with session.request("get", url) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                # print(data)
        except ClientError as err:
            # print(err)
            raise RequestError(f"Error requesting data from {url}: {err}") from err
        finally:
            if not use_running_session:
                await session.close()
        self._logger.debug("_request_data Received data for %s: %s", url, data)
        return cast(List[Dict[str, Any]], data)
    
    async def _request_loc_batt1(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_SENID_1}"
        return await self._request_data(url)
    
    async def _request_loc_batt2(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_SENID_2}"
        return await self._request_data(url)
    
    async def _request_loc_data(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_LIVEDATA}"
        return await self._request_data(url)
    
    async def _request_loc_info(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_VER}"
        return await self._request_data(url)
    
    async def _request_loc_unit(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_UNIT}"
        return await self._request_data(url)
    def locval_totemp(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=float(val)
        if unit=="0":
            val=round(val*1.8+32.0,1)
        else:
            val
        return val
    def locval_tohumi(self,val):
        val=val.replace("%","")
        return val
    def val_tobattery(self,val,unit,nty):
        if val=="" or val =="--" or val =="--.-":
            return val
        if nty=="0":
            if unit!="":
                val=f"{val} {unit}"
            else:
                val=int(val)
                if val>0 and val<=5:
                    val=f"{val*20}%"
                elif val==6:
                    val="DC"
                else:
                    val=""
        elif nty=="1":
            val=int(val)
            if val>0 and val<=5:
                 val=f"{val*20}%"
            elif val==6:
                 val="DC"
            else:
                val=""
        return val
    def locval_topress(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("hPa","")
        val=val.replace("inHg","")
        val=val.replace("mmHg","")
        val=float(val)
        if unit=="0":
            val=round((val/ 33.86388),2)  
        elif unit=="1":
            val
        else:
            val=round((val*1.33322/ 33.86388),1)  
        return val
    def locval_torain(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("in","")
        val=val.replace("mm","")
        val=val.replace("/Hr","")
        val=float(val)
        if unit=="0":
            val=round((val/ 33.86388),2)  
        return val
    def locval_tosr(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("W/m2","")
        val=val.replace("Kfc","")
        val=val.replace("Klux","")
        val=float(val)
        if unit=="0":
            val=round(( val*1000/126.7 ),2)  
        elif unit=="1":
            val
        else:
            val=round(( val*1000*10.76391/126.7 ),2)  
        return val
    def locval_towind(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("m/s","")
        val=val.replace("km/h","")
        val=val.replace("knots","")
        val=val.replace("mph","")
        val=float(val)
        if unit=="0":
            val=round(( val*2.236936 ),2)  
        elif unit=="1":
            val=round(( val/3.6 *2.236936 ),2) 
        elif unit=="2":
            val=round(( val/1.943844*2.236936 ),2) 
        else:
            val
        return val
    def locval_tolinghtdis(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("km","")
        val=val.replace("mi","")
        val=val.replace("nmi","")
        val=float(val)
        if unit=="0":
            val=round(( val* 0.62137 ),1)  
        elif unit=="1":
            val=round(( val* 0.62137 ),1) 
        elif unit=="2":
            val
        else:
            val=round(( val / 0.53996 * 0.62137 ),1) 
        return val
    async def request_loc_allinfo(self,) -> List[Dict[str, Any]]:
        res=await self._request_loc_allinfo()
        return res
    async def _request_loc_allinfo(self,) -> List[Dict[str, Any]]:
        ld_feellike= ''
        ld_dewpoint= ''
        ld_isid= ''
        ld_osid1= ''
        ld_osid2= ''
        ld_intemp= ''
        ld_inhumi= ''
        ld_outtemp= ''
        ld_outhumi= ''
        ld_abs= ''
        ld_rel= ''
        ld_wdir= ''
        ld_ws= ''
        ld_wg= ''
        ld_sr= ''
        ld_uv= ''
        ld_uvi= ''
        ld_hrr= ''
        ld_bs= ''
        ld_bs1= ''
        ld_bs2= ''
        ra_rate= ''
        ra_daily= ''
        ra_weekly= ''
        ra_month= ''
        ra_year= ''
        ra_event= ''
        piezora_rate= ''
        piezora_daily= ''
        piezora_weekly= ''
        piezora_month= ''
        piezora_year= ''
        piezora_event= ''

        cr_piezora_gain= []

        ra_prio=''
        ra_daily_retime= ''
        ra_weekly_retime= ''
        ra_year_retime= ''
        ld_is40= ''
        ld_is41= ''
        ld_is51= ''
        ld_AQI= ''
        ld_pm25ch1= ''
        ld_pm25ch2= ''
        ld_pm25ch3= ''
        ld_pm25ch4= ''
        ld_pm25ch1_AQI= ''
        ld_pm25ch2_AQI= ''
        ld_pm25ch3_AQI= ''
        ld_pm25ch4_AQI= ''
        ld_pm25ch1_24AQI= ''
        ld_pm25ch2_24AQI= ''
        ld_pm25ch3_24AQI= ''
        ld_pm25ch4_24AQI= ''
        ld_leakch1= ''
        ld_leakch2= ''
        ld_leakch3= ''
        ld_leakch4= ''
        ld_lightning= ''
        ld_lightning_time= ''
        ld_lightning_power= ''
        ld_daywindmax= ''
        ld_pm10= ''
        ld_soil= []
        ld_tempch= []
        ld_humich= []
        ld_onlytempch= []
        ld_leafch= []
        ld_co2_tf= ''
        ld_co2_humi= ''
        ld_co2_pm10= ''
        ld_co2_pm1024= ''
        ld_co2_pm25= ''
        ld_co2_pm2524= ''
        ld_co2_co2= ''
        ld_co2_co224= ''
        ld_co2_batt= ''
        ld_co2_pm10_AQI=''
        ld_co2_pm25_AQI=''

        ld_co2_co2_in= ''
        ld_co2_co224_in= ''

        ld_sen_batt=[]
        # url = f"http://{self._ip}/{GW11268_API_UNIT}"
        res_data = await self._request_loc_data()
        res_info = await self._request_loc_info()
        res_unit = await self._request_loc_unit()
        res_batt1 = await self._request_loc_batt1()
        res_batt2 = await self._request_loc_batt2()
        
        # print(res_data )
        # print(res_info )
        # print(res_unit )
        # print(res_batt1 )
        # print(res_batt2 )
        
        unit_temp=res_unit["temperature"]
        unit_press=res_unit["pressure"]
        unit_wind=res_unit["wind"]
        unit_rain=res_unit["rain"]
        unit_light=res_unit["light"]
        
        # res=(jsondata)
        # print("_request_loc_unit  : %s", res_data["common_list"])
        # if res["common_list"]:
        if "common_list" in res_data:
            for index in range(len(res_data["common_list"])):
                if res_data["common_list"][index]["id"]=='0x02':
                    ld_outtemp=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x07':
                    ld_outhumi=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x03':
                    ld_dewpoint=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x0A':
                    ld_wdir=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x0B':
                    ld_ws=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x0C':
                    ld_wg=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x15':
                    ld_sr=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x17':
                    ld_uvi=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='0x19':
                    ld_daywindmax=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='3':
                    ld_feellike=res_data["common_list"][index]["val"]
            
        if "rain" in res_data:
            for index in range(len(res_data["rain"])):   
                if res_data["rain"][index]["id"]=='0x0D':
                    ra_event=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x0E':
                    ra_rate=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x10':
                    ra_daily=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x11':
                    ra_weekly=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x12':
                    ra_month=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x13':
                    ra_year=res_data["rain"][index]["val"]
        
        if "piezoRain" in res_data:
            for index in range(len(res_data["piezoRain"])):   
                if res_data["rain"][index]["id"]=='0x0D':
                    piezora_event=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x0E':
                    piezora_rate=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x10':
                    piezora_daily=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x11':
                    piezora_weekly=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x12':
                    piezora_month=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x13':
                    piezora_year=res_data["rain"][index]["val"]
                
        if "wh25" in res_data:
            ld_intemp=res_data["wh25"][0]["intemp"]
            ld_inhumi=res_data["wh25"][0]["inhumi"]
            ld_abs=res_data["wh25"][0]["abs"]
            ld_rel=res_data["wh25"][0]["rel"]
            if "CO2" in res_data["wh25"][0]:
                ld_co2_co2_in=res_data["wh25"][0]["CO2"]
            if "CO2" in res_data["wh25"][0]:
                ld_co2_co224_in=res_data["wh25"][0]["CO2_24H"]
                
        if "lightning" in res_data:
            ld_lightning=res_data["lightning"][0]["distance"]
            ld_lightning_time=res_data["lightning"][0]["timestamp"]
            ld_lightning_power=res_data["lightning"][0]["count"]
            
        if "co2" in res_data:
             ld_co2_tf=res_data["co2"][0]["temp"]
             ld_co2_humi=res_data["co2"][0]["humidity"]
             ld_co2_pm10=res_data["co2"][0]["PM10"]
             ld_co2_pm10_AQI=res_data["co2"][0]["PM10_RealAQI"]
             ld_co2_pm1024=res_data["co2"][0]["PM10_24HAQI"]
             ld_co2_pm25=res_data["co2"][0]["PM25"]
             ld_co2_pm25_AQI=res_data["co2"][0]["PM25_RealAQI"]
             ld_co2_pm2524=res_data["co2"][0]["PM25_24HAQI"]
             ld_co2_co2=res_data["co2"][0]["CO2"]
             ld_co2_co224=res_data["co2"][0]["CO2_24H"]
             
        if "ch_pm25" in res_data:
            for index in range(len(res_data["ch_pm25"])):   
                if res_data["ch_pm25"][index]["channel"]=='1':
                    ld_pm25ch1=res_data["ch_pm25"][index]["PM25"]
                    ld_pm25ch1_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch1_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                elif res_data["ch_pm25"][index]["channel"]=='2':
                    ld_pm25ch2=res_data["ch_pm25"][index]["PM25"]
                    ld_pm25ch2_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch2_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                elif res_data["ch_pm25"][index]["channel"]=='3':
                    ld_pm25ch3=res_data["ch_pm25"][index]["PM25"]
                    ld_pm25ch3_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch3_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                elif res_data["ch_pm25"][index]["channel"]=='4':
                    ld_pm25ch4=res_data["ch_pm25"][index]["PM25"]
                    ld_pm25ch4_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch4_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                    
        if "ch_leak" in res_data:
            for index in range(len(res_data["ch_leak"])):   
                if res_data["ch_leak"][index]["channel"]=='1':
                    ld_leakch1=res_data["ch_leak"][index]["status"]
                elif res_data["ch_leak"][index]["channel"]=='2':
                    ld_leakch2=res_data["ch_leak"][index]["status"]
                elif res_data["ch_leak"][index]["channel"]=='3':
                    ld_leakch3=res_data["ch_leak"][index]["status"]
                elif res_data["ch_leak"][index]["channel"]=='4':
                    ld_leakch4=res_data["ch_leak"][index]["status"]
               
        ld_soil=[]
        ld_tempch=[]
        ld_humich=[]
        ld_onlytempch=[]
        ld_leafch=[]  
        for i in range(8):
            ld_soil.append("--")
            ld_tempch.append("--")
            ld_humich.append("--")
            ld_onlytempch.append("--")
            ld_leafch.append("--")
        
        if "ch_aisle" in res_data:
            for index in range(len(res_data["ch_aisle"])):
                ch=int(res_data["ch_aisle"][index]["channel"])-1
                ld_tempch[ch]=self.locval_totemp(res_data["ch_aisle"][index]["temp"],unit_temp)
                ld_humich[ch]=self.locval_tohumi(res_data["ch_aisle"][index]["humidity"])
                  
        if "ch_soil" in res_data:
            for index in range(len(res_data["ch_soil"])):
                ch=int(res_data["ch_soil"][index]["channel"])-1
                ld_soil[ch]=self.locval_tohumi(res_data["ch_soil"][index]["humidity"])
              
                
        if "ch_temp" in res_data:
            for index in range(len(res_data["ch_temp"])):
                ch=int(res_data["ch_temp"][index]["channel"])-1
                ld_onlytempch[ch]=self.locval_totemp(res_data["ch_temp"][index]["temp"],unit_temp)
                
                
        if "ch_leaf" in res_data:
            for index in range(len(res_data["ch_leaf"])):
                ch=int(res_data["ch_leaf"][index]["channel"])-1
                ld_leafch[ch]=self.locval_tohumi(res_data["ch_leaf"][index]["humidity"])
                
        ld_sen_batt=[]
        for i in range(58):
            ld_sen_batt.append("--")
        
        
        for index in range(len(res_batt1)):
            ch=int(res_batt1[index]["type"])
            ld_sen_batt[ch]=res_batt1[index]["batt"]
            
        for index in range(len(res_batt2)):
            ch=int(res_batt2[index]["type"])
            ld_sen_batt[ch]=res_batt2[index]["batt"]
        
                
        ver=res_info["version"][9:]
        
        
        
       
        
        # locval_totemp
        # locval_tohumi       
        # locval_topress
        # locval_torain
        # locval_tosr
        # locval_towind
        # for i in range(8):
        #     ld_soil[i]=self.locval_tohumi(ld_soil[i]),
        #     ld_tempch[i]=self.locval_totemp(ld_tempch[i],unit_temp),
        #     ld_humich[i]=self.locval_tohumi(ld_humich[i]),
        #     ld_onlytempch[i]=self.locval_totemp(ld_onlytempch[i],unit_temp),
        #     ld_leafch[i]=self.locval_tohumi(ld_leafch[i]),
        
        resjson={
            "tempinf":self.locval_totemp(ld_intemp,unit_temp),
            "humidityin":self.locval_tohumi(ld_inhumi),
            "baromrelin":self.locval_topress(ld_rel,unit_press),
            "baromabsin":self.locval_topress(ld_abs,unit_press),
            "tempf":self.locval_totemp(ld_outtemp,unit_temp),
            "humidity":self.locval_tohumi(ld_outhumi),
            "winddir":ld_wdir,
            "windspeedmph":self.locval_towind(ld_ws,unit_wind),
            "windgustmph":self.locval_towind(ld_wg,unit_wind),
            "solarradiation":self.locval_tosr(ld_sr,unit_light),
            "uv":ld_uvi,
            "daywindmax":self.locval_towind(ld_daywindmax,unit_wind),
            "feellike":self.locval_totemp(ld_feellike,unit_temp),
            "dewpoint":self.locval_totemp(ld_dewpoint,unit_temp),
            "rainratein":self.locval_torain(ra_rate,unit_rain),
            "eventrainin":self.locval_torain(ra_event,unit_rain),
            "dailyrainin":self.locval_torain(ra_daily,unit_rain),
            "weeklyrainin":self.locval_torain(ra_weekly,unit_rain),
            "monthlyrainin":self.locval_torain(ra_month,unit_rain),
            "yearlyrainin":self.locval_torain(ra_year,unit_rain),
            "rrain_piezo":self.locval_torain(piezora_rate,unit_rain),
            "erain_piezo":self.locval_torain(piezora_event,unit_rain),
            "drain_piezo":self.locval_torain(piezora_daily,unit_rain),
            "wrain_piezo":self.locval_torain(piezora_weekly,unit_rain),
            "mrain_piezo":self.locval_torain(piezora_month,unit_rain),
            "yrain_piezo":self.locval_torain(piezora_year,unit_rain),
            "pm25_ch1":ld_pm25ch1,
            "pm25_ch2":ld_pm25ch2,
            "pm25_ch3":ld_pm25ch3,
            "pm25_ch4":ld_pm25ch4,
            "pm25_aqi_ch1":ld_pm25ch1_AQI,
            "pm25_aqi_ch2":ld_pm25ch2_AQI,
            "pm25_aqi_ch3":ld_pm25ch3_AQI,
            "pm25_aqi_ch4":ld_pm25ch4_AQI,
            "pm25_avg_24h_ch1":ld_pm25ch1_24AQI,
            "pm25_avg_24h_ch2":ld_pm25ch2_24AQI,
            "pm25_avg_24h_ch3":ld_pm25ch3_24AQI,
            "pm25_avg_24h_ch4":ld_pm25ch4_24AQI,
            "co2in":ld_co2_co2_in,
            "co2in_24h":ld_co2_co224_in,
            "co2":ld_co2_co2,
            "co2_24h":ld_co2_co224,
            "pm25_co2":ld_co2_pm25,
            "pm25_24h_co2":ld_co2_pm2524,
            "pm10_co2":ld_co2_pm10,
            "pm10_24h_co2":ld_co2_pm1024,
            "pm10_aqi_co2":ld_co2_pm10_AQI,
            "pm25_aqi_co2":ld_co2_pm25_AQI,
            "tf_co2":self.locval_totemp(ld_co2_tf,unit_temp),
            "humi_co2":self.locval_tohumi(ld_co2_humi),
            "lightning":self.locval_tolinghtdis(ld_lightning,unit_wind),
            "lightning_time":ld_lightning_time,
            "lightning_num":ld_lightning_power,
            "leak_ch1":ld_leakch1,
            "leak_ch2":ld_leakch2,
            "leak_ch3":ld_leakch3,
            "leak_ch4":ld_leakch4,
            "temp_ch1":ld_tempch[0],
            "temp_ch2":ld_tempch[1],
            "temp_ch3":ld_tempch[2],
            "temp_ch4":ld_tempch[3],
            "temp_ch5":ld_tempch[4],
            "temp_ch6":ld_tempch[5],
            "temp_ch7":ld_tempch[6],
            "temp_ch8":ld_tempch[7],
            "humidity_ch1":ld_humich[0],
            "humidity_ch2":ld_humich[1],
            "humidity_ch3":ld_humich[2],
            "humidity_ch4":ld_humich[3],
            "humidity_ch5":ld_humich[4],
            "humidity_ch6":ld_humich[5],
            "humidity_ch7":ld_humich[6],
            "humidity_ch8":ld_humich[7],
            "Soilmoisture_ch1":ld_soil[0],
            "Soilmoisture_ch2":ld_soil[1],
            "Soilmoisture_ch3":ld_soil[2],
            "Soilmoisture_ch4":ld_soil[3],
            "Soilmoisture_ch5":ld_soil[4],
            "Soilmoisture_ch6":ld_soil[5],
            "Soilmoisture_ch7":ld_soil[6],
            "Soilmoisture_ch8":ld_soil[7],
            "tf_ch1":ld_onlytempch[0],
            "tf_ch2":ld_onlytempch[1],
            "tf_ch3":ld_onlytempch[2],
            "tf_ch4":ld_onlytempch[3],
            "tf_ch5":ld_onlytempch[4],
            "tf_ch6":ld_onlytempch[5],
            "tf_ch7":ld_onlytempch[6],
            "tf_ch8":ld_onlytempch[7],
            "leaf_ch1":ld_leafch[0],
            "leaf_ch2":ld_leafch[1],
            "leaf_ch3":ld_leafch[2],
            "leaf_ch4":ld_leafch[3],
            "leaf_ch5":ld_leafch[4],
            "leaf_ch6":ld_leafch[5],
            "leaf_ch7":ld_leafch[6],
            "leaf_ch8":ld_leafch[7],
            "ver":ver,
            # "allbatt":ld_sen_batt,
            "pm25_ch1_batt":self.val_tobattery(ld_sen_batt[22],"","1"),
            "pm25_ch2_batt":self.val_tobattery(ld_sen_batt[23],"","1"),
            "pm25_ch3_batt":self.val_tobattery(ld_sen_batt[24],"","1"),
            "pm25_ch4_batt":self.val_tobattery(ld_sen_batt[25],"","1"),
            "leak_ch1_batt":self.val_tobattery(ld_sen_batt[27],"","1"),
            "leak_ch2_batt":self.val_tobattery(ld_sen_batt[28],"","1"),
            "leak_ch3_batt":self.val_tobattery(ld_sen_batt[29],"","1"),
            "leak_ch4_batt":self.val_tobattery(ld_sen_batt[30],"","1"),
            "temph_ch1_batt":self.val_tobattery(ld_sen_batt[6] ,"","1"),
            "temph_ch2_batt":self.val_tobattery(ld_sen_batt[7] ,"","1"),
            "temph_ch3_batt":self.val_tobattery(ld_sen_batt[8] ,"","1"),
            "temph_ch4_batt":self.val_tobattery(ld_sen_batt[9] ,"","1"),
            "temph_ch5_batt":self.val_tobattery(ld_sen_batt[10] ,"","1"),
            "temph_ch6_batt":self.val_tobattery(ld_sen_batt[11],"","1"),
            "temph_ch7_batt":self.val_tobattery(ld_sen_batt[12],"","1"),
            "temph_ch8_batt":self.val_tobattery(ld_sen_batt[13],"","1"),
            "Soilmoisture_ch1_batt":self.val_tobattery(ld_sen_batt[14],"","1"),
            "Soilmoisture_ch2_batt":self.val_tobattery(ld_sen_batt[15],"","1"),
            "Soilmoisture_ch3_batt":self.val_tobattery(ld_sen_batt[16],"","1"),
            "Soilmoisture_ch4_batt":self.val_tobattery(ld_sen_batt[17],"","1"),
            "Soilmoisture_ch5_batt":self.val_tobattery(ld_sen_batt[18],"","1"),
            "Soilmoisture_ch6_batt":self.val_tobattery(ld_sen_batt[19],"","1"),
            "Soilmoisture_ch7_batt":self.val_tobattery(ld_sen_batt[20],"","1"),
            "Soilmoisture_ch8_batt":self.val_tobattery(ld_sen_batt[21],"","1"),
            "tf_ch1_batt":self.val_tobattery(ld_sen_batt[31],"","1"),
            "tf_ch2_batt":self.val_tobattery(ld_sen_batt[32],"","1"),
            "tf_ch3_batt":self.val_tobattery(ld_sen_batt[33],"","1"),
            "tf_ch4_batt":self.val_tobattery(ld_sen_batt[34],"","1"),
            "tf_ch5_batt":self.val_tobattery(ld_sen_batt[35],"","1"),
            "tf_ch6_batt":self.val_tobattery(ld_sen_batt[36],"","1"),
            "tf_ch7_batt":self.val_tobattery(ld_sen_batt[37],"","1"),
            "tf_ch8_batt":self.val_tobattery(ld_sen_batt[38],"","1"),
            "leaf_ch1_batt":self.val_tobattery(ld_sen_batt[40],"","1"),
            "leaf_ch2_batt":self.val_tobattery(ld_sen_batt[41],"","1"),
            "leaf_ch3_batt":self.val_tobattery(ld_sen_batt[42],"","1"),
            "leaf_ch4_batt":self.val_tobattery(ld_sen_batt[43],"","1"),
            "leaf_ch5_batt":self.val_tobattery(ld_sen_batt[44],"","1"),
            "leaf_ch6_batt":self.val_tobattery(ld_sen_batt[45],"","1"),
            "leaf_ch7_batt":self.val_tobattery(ld_sen_batt[46],"","1"),
            "leaf_ch8_batt":self.val_tobattery(ld_sen_batt[47],"","1"),
            
        }
        
        # batt pm25 index 22-25
        # batt leak index 27-30
        # batt t&h index 5-12
        # batt soil index 13-20
        # batt onlytemp index 30-37
        # batt leaf index 39-46
               
        # for x in resjson.items():  
        #     print(x[0],x[1])
                    
        
        # print(ver )
        # print(resjson )
        return resjson