"""Define an object to interact with the REST API."""
from ast import For
import asyncio
from datetime import date
import enum
from http.client import SWITCHING_PROTOCOLS
import logging
from typing import Any, Dict, List, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
import time
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
GW11268_API_SYS = "get_device_info"
GW11268_API_MAC = "get_network_info"

DEFAULT_LIMIT = 288
DEFAULT_TIMEOUT = 20

TYPE_TEMPINF = "tempinf"
TYPE_HUMIDITYIN = "humidityin"
TYPE_REL = "baromrelin"
TYPE_ABS = "baromabsin"
TYPE_TEMPOUT = "tempf"
TYPE_HUMIOUT = "humidity"
TYPE_WDIR = "winddir"
TYPE_WDIR10 = "winddir10"
TYPE_VPD = "vpd"
TYPE_APPARE = "apparent"
TYPE_WS = "windspeedmph"
TYPE_WG = "windgustmph"
TYPE_SR = "solarradiation"
TYPE_UV = "uv"
TYPE_DWM = "daywindmax"
TYPE_FEELLIKE = "feellike"
TYPE_DEWP = "dewpoint"
TYPE_RR = "rainratein"
TYPE_ER = "eventrainin"
TYPE_DR = "dailyrainin"
TYPE_WR = "weeklyrainin"
TYPE_MR = "monthlyrainin"
TYPE_YR = "yearlyrainin"
TYPE_TR = "totalrainin"
TYPE_24R = "24hrainin"
TYPE_PIEZO_RR = "rrain_piezo"
TYPE_PIEZO_ER = "erain_piezo"
TYPE_PIEZO_DR = "drain_piezo"
TYPE_PIEZO_WR = "wrain_piezo"
TYPE_PIEZO_MR = "mrain_piezo"
TYPE_PIEZO_YR = "yrain_piezo"
TYPE_PIEZO_TR = "train_piezo"
TYPE_PIEZO_24R = "rain_piezo24h"
TYPE_PM25CH1 = "pm25_ch1"
TYPE_PM25CH2 = "pm25_ch2"
TYPE_PM25CH3 = "pm25_ch3"
TYPE_PM25CH4 = "pm25_ch4"
TYPE_PM25RTAQICH1 = "pm25_aqi_ch1"
TYPE_PM25RTAQICH2 = "pm25_aqi_ch2"
TYPE_PM25RTAQICH3 = "pm25_aqi_ch3"
TYPE_PM25RTAQICH4 = "pm25_aqi_ch4"
TYPE_PM2524HAQICH1 = "pm25_avg_24h_ch1"
TYPE_PM2524HAQICH2 = "pm25_avg_24h_ch2"
TYPE_PM2524HAQICH3 = "pm25_avg_24h_ch3"
TYPE_PM2524HAQICH4 = "pm25_avg_24h_ch4"
TYPE_CO2IN = "co2in"
TYPE_CO224HIN = "co2in_24h"
TYPE_CO2OUT = "co2"
TYPE_CO224HOUT = "co2_24h"
TYPE_CO2PM25 = "pm25_co2"
TYPE_CO224HPM25 = "pm25_24h_co2"
TYPE_CO2PM10 = "pm10_co2"
TYPE_CO224HPM10 = "pm10_24h_co2"
TYPE_CO2RTPM10 = "pm10_aqi_co2"
TYPE_CO2RTPM25 = "pm25_aqi_co2"
TYPE_CO2TEMP = "tf_co2"
TYPE_CO2HUMI = "humi_co2"
TYPE_LIGHTNING = "lightning"
TYPE_LIGHTNINGTIME = "lightning_time"
TYPE_LIGHTNINGNUM = "lightning_num"
TYPE_LEAKCH1 = "leak_ch1"
TYPE_LEAKCH2 = "leak_ch2"
TYPE_LEAKCH3 = "leak_ch3"
TYPE_LEAKCH4 = "leak_ch4"
TYPE_TEMPCH1 = "temp_ch1"
TYPE_TEMPCH2 = "temp_ch2"
TYPE_TEMPCH3 = "temp_ch3"
TYPE_TEMPCH4 = "temp_ch4"
TYPE_TEMPCH5 = "temp_ch5"
TYPE_TEMPCH6 = "temp_ch6"
TYPE_TEMPCH7 = "temp_ch7"
TYPE_TEMPCH8 = "temp_ch8"
TYPE_HUMICH1 = "humidity_ch1"
TYPE_HUMICH2 = "humidity_ch2"
TYPE_HUMICH3 = "humidity_ch3"
TYPE_HUMICH4 = "humidity_ch4"
TYPE_HUMICH5 = "humidity_ch5"
TYPE_HUMICH6 = "humidity_ch6"
TYPE_HUMICH7 = "humidity_ch7"
TYPE_HUMICH8 = "humidity_ch8"
TYPE_SOILCH1 = "Soilmoisture_ch1"
TYPE_SOILCH2 = "Soilmoisture_ch2"
TYPE_SOILCH3 = "Soilmoisture_ch3"
TYPE_SOILCH4 = "Soilmoisture_ch4"
TYPE_SOILCH5 = "Soilmoisture_ch5"
TYPE_SOILCH6 = "Soilmoisture_ch6"
TYPE_SOILCH7 = "Soilmoisture_ch7"
TYPE_SOILCH8 = "Soilmoisture_ch8"
TYPE_SOILCH9 = "Soilmoisture_ch9"
TYPE_SOILCH10 = "Soilmoisture_ch10"
TYPE_SOILCH11 = "Soilmoisture_ch11"
TYPE_SOILCH12 = "Soilmoisture_ch12"
TYPE_SOILCH13 = "Soilmoisture_ch13"
TYPE_SOILCH14 = "Soilmoisture_ch14"
TYPE_SOILCH15 = "Soilmoisture_ch15"
TYPE_SOILCH16 = "Soilmoisture_ch16"
TYPE_ONLYTEMPCH1 = "tf_ch1"
TYPE_ONLYTEMPCH2 = "tf_ch2"
TYPE_ONLYTEMPCH3 = "tf_ch3"
TYPE_ONLYTEMPCH4 = "tf_ch4"
TYPE_ONLYTEMPCH5 = "tf_ch5"
TYPE_ONLYTEMPCH6 = "tf_ch6"
TYPE_ONLYTEMPCH7 = "tf_ch7"
TYPE_ONLYTEMPCH8 = "tf_ch8"
TYPE_LEAFCH1 = "leaf_ch1"
TYPE_LEAFCH2 = "leaf_ch2"
TYPE_LEAFCH3 = "leaf_ch3"
TYPE_LEAFCH4 = "leaf_ch4"
TYPE_LEAFCH5 = "leaf_ch5"
TYPE_LEAFCH6 = "leaf_ch6"
TYPE_LEAFCH7 = "leaf_ch7"
TYPE_LEAFCH8 = "leaf_ch8"
TYPE_LDSAIRCH1 = "lds_air_ch1"
TYPE_LDSAIRCH2 = "lds_air_ch2"
TYPE_LDSAIRCH3 = "lds_air_ch3"
TYPE_LDSAIRCH4 = "lds_air_ch4"
TYPE_LDSDEPCH1 = "lds_dep_ch1"
TYPE_LDSDEPCH2 = "lds_dep_ch2"
TYPE_LDSDEPCH3 = "lds_dep_ch3"
TYPE_LDSDEPCH4 = "lds_dep_ch4"
TYPE_LDSHEATCH1 = "lds_heat_ch1"
TYPE_LDSHEATCH2 = "lds_heat_ch2"
TYPE_LDSHEATCH3 = "lds_heat_ch3"
TYPE_LDSHEATCH4 = "lds_heat_ch4"

TYPE_PM25CH1_BATT = "pm25_ch1_batt"
TYPE_PM25CH2_BATT = "pm25_ch2_batt"
TYPE_PM25CH3_BATT = "pm25_ch3_batt"
TYPE_PM25CH4_BATT = "pm25_ch4_batt"
TYPE_LEAKCH1_BATT = "leak_ch1_batt"
TYPE_LEAKCH2_BATT = "leak_ch2_batt"
TYPE_LEAKCH3_BATT = "leak_ch3_batt"
TYPE_LEAKCH4_BATT = "leak_ch4_batt"
TYPE_TEMPCH1_BATT = "temph_ch1_batt"
TYPE_TEMPCH2_BATT = "temph_ch2_batt"
TYPE_TEMPCH3_BATT = "temph_ch3_batt"
TYPE_TEMPCH4_BATT = "temph_ch4_batt"
TYPE_TEMPCH5_BATT = "temph_ch5_batt"
TYPE_TEMPCH6_BATT = "temph_ch6_batt"
TYPE_TEMPCH7_BATT = "temph_ch7_batt"
TYPE_TEMPCH8_BATT = "temph_ch8_batt"
TYPE_SOILCH1_BATT = "Soilmoisture_ch1_batt"
TYPE_SOILCH2_BATT = "Soilmoisture_ch2_batt"
TYPE_SOILCH3_BATT = "Soilmoisture_ch3_batt"
TYPE_SOILCH4_BATT = "Soilmoisture_ch4_batt"
TYPE_SOILCH5_BATT = "Soilmoisture_ch5_batt"
TYPE_SOILCH6_BATT = "Soilmoisture_ch6_batt"
TYPE_SOILCH7_BATT = "Soilmoisture_ch7_batt"
TYPE_SOILCH8_BATT = "Soilmoisture_ch8_batt"
TYPE_SOILCH9_BATT = "Soilmoisture_ch9_batt"
TYPE_SOILCH10_BATT = "Soilmoisture_ch10_batt"
TYPE_SOILCH11_BATT = "Soilmoisture_ch11_batt"
TYPE_SOILCH12_BATT = "Soilmoisture_ch12_batt"
TYPE_SOILCH13_BATT = "Soilmoisture_ch13_batt"
TYPE_SOILCH14_BATT = "Soilmoisture_ch14_batt"
TYPE_SOILCH15_BATT = "Soilmoisture_ch15_batt"
TYPE_SOILCH16_BATT = "Soilmoisture_ch16_batt"
TYPE_ONLYTEMPCH1_BATT = "tf_ch1_batt"
TYPE_ONLYTEMPCH2_BATT = "tf_ch2_batt"
TYPE_ONLYTEMPCH3_BATT = "tf_ch3_batt"
TYPE_ONLYTEMPCH4_BATT = "tf_ch4_batt"
TYPE_ONLYTEMPCH5_BATT = "tf_ch5_batt"
TYPE_ONLYTEMPCH6_BATT = "tf_ch6_batt"
TYPE_ONLYTEMPCH7_BATT = "tf_ch7_batt"
TYPE_ONLYTEMPCH8_BATT = "tf_ch8_batt"
TYPE_LEAFCH1_BATT = "leaf_ch1_batt"
TYPE_LEAFCH2_BATT = "leaf_ch2_batt"
TYPE_LEAFCH3_BATT = "leaf_ch3_batt"
TYPE_LEAFCH4_BATT = "leaf_ch4_batt"
TYPE_LEAFCH5_BATT = "leaf_ch5_batt"
TYPE_LEAFCH6_BATT = "leaf_ch6_batt"
TYPE_LEAFCH7_BATT = "leaf_ch7_batt"
TYPE_LEAFCH8_BATT = "leaf_ch8_batt"
TYPE_LDSCH1_BATT = "lds_ch1_batt"
TYPE_LDSCH2_BATT = "lds_ch2_batt"
TYPE_LDSCH3_BATT = "lds_ch3_batt"
TYPE_LDSCH4_BATT = "lds_ch4_batt"

class WittiotDataTypes(enum.Enum):
    """Wittiot Data types."""
    TEMPERATURE=1
    HUMIDITY = 2
    PM25 = 3
    AQI=4
    LEAK = 5
    BATTERY = 6
    DISTANCE = 7
    HEAT = 8



class MultiSensorInfo:
    """Multi Sensor Info."""

    SENSOR_INFO={
        TYPE_PM25CH1 : {"dev_type": "CH1 PM25","name":"CH1 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25CH2 : {"dev_type": "CH2 PM25","name":"CH2 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25CH3 : {"dev_type": "CH3 PM25","name":"CH3 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25CH4 : {"dev_type": "CH4 PM25","name":"CH4 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25RTAQICH1 : {"dev_type": "CH1 PM25","name":"CH1 PM2.5 AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM25RTAQICH2 : {"dev_type": "CH2 PM25","name":"CH2 PM2.5 AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM25RTAQICH3 : {"dev_type": "CH3 PM25","name":"CH3 PM2.5 AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM25RTAQICH4 : {"dev_type": "CH4 PM25","name":"CH4 PM2.5 AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM2524HAQICH1 : {"dev_type": "CH1 PM25","name":"CH1 PM2.5 24H AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM2524HAQICH2 : {"dev_type": "CH2 PM25","name":"CH2 PM2.5 24H AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM2524HAQICH3 : {"dev_type": "CH3 PM25","name":"CH3 PM2.5 24H AQI","data_type":WittiotDataTypes.AQI},
        TYPE_PM2524HAQICH4 : {"dev_type": "CH4 PM25","name":"CH4 PM2.5 24H AQI","data_type":WittiotDataTypes.AQI},
        TYPE_LEAKCH1 : {"dev_type": "CH1 LEAK","name":"CH1 LEAK","data_type":WittiotDataTypes.LEAK},
        TYPE_LEAKCH2 : {"dev_type": "CH2 LEAK","name":"CH2 LEAK","data_type":WittiotDataTypes.LEAK},
        TYPE_LEAKCH3 : {"dev_type": "CH3 LEAK","name":"CH3 LEAK","data_type":WittiotDataTypes.LEAK},
        TYPE_LEAKCH4 : {"dev_type": "CH4 LEAK","name":"CH4 LEAK","data_type":WittiotDataTypes.LEAK},
        TYPE_TEMPCH1 : {"dev_type": "CH1 T&H","name":"CH1 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH2 : {"dev_type": "CH2 T&H","name":"CH2 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH3 : {"dev_type": "CH3 T&H","name":"CH3 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH4 : {"dev_type": "CH4 T&H","name":"CH4 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH5 : {"dev_type": "CH5 T&H","name":"CH5 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH6 : {"dev_type": "CH6 T&H","name":"CH6 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH7 : {"dev_type": "CH7 T&H","name":"CH7 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_TEMPCH8 : {"dev_type": "CH8 T&H","name":"CH8 T&H Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_HUMICH1 : {"dev_type": "CH1 T&H","name":"CH1 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH2 : {"dev_type": "CH2 T&H","name":"CH2 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH3 : {"dev_type": "CH3 T&H","name":"CH3 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH4 : {"dev_type": "CH4 T&H","name":"CH4 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH5 : {"dev_type": "CH5 T&H","name":"CH5 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH6 : {"dev_type": "CH6 T&H","name":"CH6 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH7 : {"dev_type": "CH7 T&H","name":"CH7 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_HUMICH8 : {"dev_type": "CH8 T&H","name":"CH8 T&H Humidity","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH1 : {"dev_type": "CH1 Soil","name":"CH1 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH2 : {"dev_type": "CH2 Soil","name":"CH2 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH3 : {"dev_type": "CH3 Soil","name":"CH3 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH4 : {"dev_type": "CH4 Soil","name":"CH4 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH5 : {"dev_type": "CH5 Soil","name":"CH5 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH6 : {"dev_type": "CH6 Soil","name":"CH6 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH7 : {"dev_type": "CH7 Soil","name":"CH7 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH8 : {"dev_type": "CH8 Soil","name":"CH8 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH9 : {"dev_type": "CH9 Soil","name":"CH9 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH10 : {"dev_type": "CH10 Soil","name":"CH10 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH11 : {"dev_type": "CH11 Soil","name":"CH11 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH12 : {"dev_type": "CH12 Soil","name":"CH12 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH13 : {"dev_type": "CH13 Soil","name":"CH13 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH14 : {"dev_type": "CH14 Soil","name":"CH14 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH15 : {"dev_type": "CH15 Soil","name":"CH15 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_SOILCH16 : {"dev_type": "CH16 Soil","name":"CH16 Soil","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_ONLYTEMPCH1 : {"dev_type": "CH1 Temp","name":"CH1 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH2 : {"dev_type": "CH2 Temp","name":"CH2 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH3 : {"dev_type": "CH3 Temp","name":"CH3 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH4 : {"dev_type": "CH4 Temp","name":"CH4 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH5 : {"dev_type": "CH5 Temp","name":"CH5 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH6 : {"dev_type": "CH6 Temp","name":"CH6 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH7 : {"dev_type": "CH7 Temp","name":"CH7 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_ONLYTEMPCH8 : {"dev_type": "CH8 Temp","name":"CH8 Temp","data_type":WittiotDataTypes.TEMPERATURE},
        TYPE_LEAFCH1 : {"dev_type": "CH1 Leaf","name":"CH1 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH2 : {"dev_type": "CH2 Leaf","name":"CH2 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH3 : {"dev_type": "CH3 Leaf","name":"CH3 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH4 : {"dev_type": "CH4 Leaf","name":"CH4 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH5 : {"dev_type": "CH5 Leaf","name":"CH5 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH6 : {"dev_type": "CH6 Leaf","name":"CH6 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH7 : {"dev_type": "CH7 Leaf","name":"CH7 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LEAFCH8 : {"dev_type": "CH8 Leaf","name":"CH8 Leaf","data_type":WittiotDataTypes.HUMIDITY},
        TYPE_LDSAIRCH1 : {"dev_type": "CH1 Lds","name":"CH1 Air","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSAIRCH2 : {"dev_type": "CH2 Lds","name":"CH2 Air","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSAIRCH3 : {"dev_type": "CH3 Lds","name":"CH3 Air","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSAIRCH4 : {"dev_type": "CH4 Lds","name":"CH4 Air","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSDEPCH1 : {"dev_type": "CH1 Lds","name":"CH1 Depth","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSDEPCH2 : {"dev_type": "CH2 Lds","name":"CH2 Depth","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSDEPCH3 : {"dev_type": "CH3 Lds","name":"CH3 Depth","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSDEPCH4 : {"dev_type": "CH4 Lds","name":"CH4 Depth","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSHEATCH1 : {"dev_type": "CH1 Lds","name":"CH1 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_LDSHEATCH2 : {"dev_type": "CH2 Lds","name":"CH2 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_LDSHEATCH3 : {"dev_type": "CH3 Lds","name":"CH3 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_LDSHEATCH4 : {"dev_type": "CH4 Lds","name":"CH4 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_PM25CH1_BATT : {"dev_type": "CH1 PM25","name":"CH1 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_PM25CH2_BATT : {"dev_type": "CH2 PM25","name":"CH2 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_PM25CH3_BATT : {"dev_type": "CH3 PM25","name":"CH3 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_PM25CH4_BATT : {"dev_type": "CH4 PM25","name":"CH4 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH1_BATT : {"dev_type": "CH1 LEAK","name":"CH1 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH2_BATT : {"dev_type": "CH2 LEAK","name":"CH2 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH3_BATT : {"dev_type": "CH3 LEAK","name":"CH3 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH4_BATT : {"dev_type": "CH4 LEAK","name":"CH4 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH1_BATT : {"dev_type": "CH1 T&H","name":"CH1 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH2_BATT : {"dev_type": "CH2 T&H","name":"CH2 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH3_BATT : {"dev_type": "CH3 T&H","name":"CH3 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH4_BATT : {"dev_type": "CH4 T&H","name":"CH4 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH5_BATT : {"dev_type": "CH5 T&H","name":"CH5 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH6_BATT : {"dev_type": "CH6 T&H","name":"CH6 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH7_BATT : {"dev_type": "CH7 T&H","name":"CH7 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH8_BATT : {"dev_type": "CH8 T&H","name":"CH8 T&H Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH1_BATT : {"dev_type": "CH1 Soil","name":"CH1 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH2_BATT : {"dev_type": "CH2 Soil","name":"CH2 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH3_BATT : {"dev_type": "CH3 Soil","name":"CH3 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH4_BATT : {"dev_type": "CH4 Soil","name":"CH4 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH5_BATT : {"dev_type": "CH5 Soil","name":"CH5 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH6_BATT : {"dev_type": "CH6 Soil","name":"CH6 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH7_BATT : {"dev_type": "CH7 Soil","name":"CH7 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH8_BATT : {"dev_type": "CH8 Soil","name":"CH8 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH9_BATT : {"dev_type": "CH9 Soil","name":"CH9 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH10_BATT : {"dev_type": "CH10 Soil","name":"CH10 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH11_BATT : {"dev_type": "CH11 Soil","name":"CH11 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH12_BATT : {"dev_type": "CH12 Soil","name":"CH12 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH13_BATT : {"dev_type": "CH13 Soil","name":"CH13 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH14_BATT : {"dev_type": "CH14 Soil","name":"CH14 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH15_BATT : {"dev_type": "CH15 Soil","name":"CH15 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_SOILCH16_BATT : {"dev_type": "CH16 Soil","name":"CH16 Soil Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH1_BATT : {"dev_type": "CH1 Temp","name":"CH1 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH2_BATT : {"dev_type": "CH2 Temp","name":"CH2 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH3_BATT : {"dev_type": "CH3 Temp","name":"CH3 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH4_BATT : {"dev_type": "CH4 Temp","name":"CH4 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH5_BATT : {"dev_type": "CH5 Temp","name":"CH5 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH6_BATT : {"dev_type": "CH6 Temp","name":"CH6 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH7_BATT : {"dev_type": "CH7 Temp","name":"CH7 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_ONLYTEMPCH8_BATT : {"dev_type": "CH8 Temp","name":"CH8 Temp Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH1_BATT : {"dev_type": "CH1 Leaf","name":"CH1 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH2_BATT : {"dev_type": "CH2 Leaf","name":"CH2 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH3_BATT : {"dev_type": "CH3 Leaf","name":"CH3 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH4_BATT : {"dev_type": "CH4 Leaf","name":"CH4 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH5_BATT : {"dev_type": "CH5 Leaf","name":"CH5 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH6_BATT : {"dev_type": "CH6 Leaf","name":"CH6 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH7_BATT : {"dev_type": "CH7 Leaf","name":"CH7 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAFCH8_BATT : {"dev_type": "CH8 Leaf","name":"CH8 Leaf Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LDSCH1_BATT : {"dev_type": "CH1 Lds","name":"CH1 Lds Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LDSCH2_BATT : {"dev_type": "CH2 Lds","name":"CH2 Lds Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LDSCH3_BATT : {"dev_type": "CH3 Lds","name":"CH3 Lds Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LDSCH4_BATT : {"dev_type": "CH4 Lds","name":"CH4 Lds Battery","data_type":WittiotDataTypes.BATTERY},
    }

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
    async def _request_loc_sys(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_SYS}"
        return await self._request_data(url)
    async def _request_loc_mac(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_MAC}"
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
    def locval_tolds(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("mm","")
        val=val.replace("ft","")
        val=float(val)
        if unit=="0":
            val=round(val/304.8,2)
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
    def locval_topressmk2(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("kPa","")
        val=val.replace("inHg","")
        val=val.replace("mmHg","")
        val=float(val)
        if unit=="0":
            val=round((val/ 3.386388),3)
        elif unit=="1":
            val
        else:
            val=round((val*1.33322/ 33.86388),3)
        return val
    def locval_torain(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("in","")
        val=val.replace("mm","")
        val=val.replace("/Hr","")
        val=float(val)
        if unit=="0":
            val=round((val/ 25.4),2)
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
    def get_min_wind_speed(self,bft_level):
        # 蒲福风级与最小风速对应表
        bft_level=int(bft_level)
        bft_to_min_speed = {
            0: 0.0,    # 无风
            1: 1.0,    # 软风
            2: 4.0,    # 轻风
            3: 8.0,    # 微风
            4: 13.0,   # 和风
            5: 19.0,   # 清风
            6: 24.0,   # 强风
            7: 31.0,   # 疾风
            8: 39.0,   # 大风
            9: 47.0,   # 烈风
            10: 55.0,  # 狂风
            11: 63.0,  # 暴风
            12: 74.0   # 飓风
        }
        return bft_to_min_speed[bft_level]
    
    def locval_towind(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("m/s","")
        val=val.replace("km/h","")
        val=val.replace("knots","")
        val=val.replace("mph","")
        val=val.replace("BFT","")
        val=val.replace("ft/s","")
        val=float(val)
        if unit=="0":
            val=round(( val*2.236936 ),2)
        elif unit=="1":
            val=round(( val*0.621371 ),2)
        elif unit=="3":
            val=round(( val*1.15078 ),2)
        elif unit=="5":
            val=self.get_min_wind_speed(val)
        # elif unit=="5":
        #     val=round(( val/1.466667 ),2)
        else:
            val
        return val
    def locval_tolinghtdis(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        val=val.replace("km","")
        val=val.replace("nmi","")
        val=val.replace("mi","")
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
    async def request_loc_info(self,) -> List[Dict[str, Any]]:
        # res=await self._request_loc_info()
        res_info = await self._request_loc_info()
        res_sys = await self._request_loc_sys()
        res_mac = await self._request_loc_mac()

        resjson={
            'version':res_info["version"][9:],
            'dev_name':res_sys["apName"],
            'mac':res_mac["mac"],
        }
        return resjson
    async def _request_loc_allinfo(self,) -> List[Dict[str, Any]]:
        # time.sleep(15)
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
        ld_wdir10= ''
        ld_apparent= ''
        ld_vpd= ''
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
        ra_total= ''	
        ra_24hour= ''
        piezora_rate= ''
        piezora_daily= ''
        piezora_weekly= ''
        piezora_month= ''
        piezora_year= ''
        piezora_event= ''
        piezora_total= ''	
        piezora_24hour= ''


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
        ld_lds_airch= []
        ld_lds_depthch= []
        ld_lds_heatch= []
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
        res_sys = await self._request_loc_sys()
        res_mac = await self._request_loc_mac()

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
                elif res_data["common_list"][index]["id"]=='0x6D':
                    ld_wdir10=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='4':
                    ld_apparent=res_data["common_list"][index]["val"]
                elif res_data["common_list"][index]["id"]=='5':
                    ld_vpd=res_data["common_list"][index]["val"]

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
                elif res_data["rain"][index]["id"]=='0x14':
                    ra_total=res_data["rain"][index]["val"]
                elif res_data["rain"][index]["id"]=='0x7C':
                    ra_24hour=res_data["rain"][index]["val"]

        if "piezoRain" in res_data:
            for index in range(len(res_data["piezoRain"])):
                if res_data["piezoRain"][index]["id"]=='0x0D':
                    piezora_event=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x0E':
                    piezora_rate=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x10':
                    piezora_daily=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x11':
                    piezora_weekly=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x12':
                    piezora_month=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x13':
                    piezora_year=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x14':
                    piezora_total=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x7C':
                    piezora_24hour=res_data["piezoRain"][index]["val"]

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
        ld_lds_airch=[]
        ld_lds_depthch=[]
        ld_lds_heatch=[]
        for i in range(16):
            ld_soil.append("--")
            ld_tempch.append("--")
            ld_humich.append("--")
            ld_onlytempch.append("--")
            ld_leafch.append("--")
            ld_lds_airch.append("--")
            ld_lds_depthch.append("--")
            ld_lds_heatch.append("--")

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
                
        if "ch_lds" in res_data:
            for index in range(len(res_data["ch_lds"])):
                ch=int(res_data["ch_lds"][index]["channel"])-1
                ld_lds_airch[ch]=self.locval_tolds(res_data["ch_lds"][index]["air"],unit_rain)
                ld_lds_depthch[ch]=self.locval_tolds(res_data["ch_lds"][index]["depth"],unit_rain)
                ld_lds_heatch[ch]=res_data["ch_lds"][index].get("total_heat", "--")

        ld_sen_batt=[]
        for i in range(99):
            ld_sen_batt.append("--")


        for index in range(len(res_batt1)):
            ch=int(res_batt1[index]["type"])
            ld_sen_batt[ch]=res_batt1[index]["batt"]

        for index in range(len(res_batt2)):
            ch=int(res_batt2[index]["type"])
            ld_sen_batt[ch]=res_batt2[index]["batt"]


        ver=res_info["version"][9:]
        devname=res_sys["apName"]
        mac=res_mac["mac"]



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
            "winddir10":ld_wdir10,
            "apparent":self.locval_totemp(ld_apparent,unit_temp),
            "vpd":self.locval_topressmk2(ld_vpd,unit_press),
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
            "totalrainin":self.locval_torain(ra_total,unit_rain),
            "24hrainin":self.locval_torain(ra_24hour,unit_rain),
            "rrain_piezo":self.locval_torain(piezora_rate,unit_rain),
            "erain_piezo":self.locval_torain(piezora_event,unit_rain),
            "drain_piezo":self.locval_torain(piezora_daily,unit_rain),
            "wrain_piezo":self.locval_torain(piezora_weekly,unit_rain),
            "mrain_piezo":self.locval_torain(piezora_month,unit_rain),
            "yrain_piezo":self.locval_torain(piezora_year,unit_rain),
            "train_piezo":self.locval_torain(piezora_total,unit_rain),
            "24hrain_piezo":self.locval_torain(piezora_24hour,unit_rain),
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
            "lds_air_ch1":ld_lds_airch[0],
            "lds_air_ch2":ld_lds_airch[1],
            "lds_air_ch3":ld_lds_airch[2],
            "lds_air_ch4":ld_lds_airch[3],
            "lds_depth_ch1":ld_lds_depthch[0],
            "lds_depth_ch2":ld_lds_depthch[1],
            "lds_depth_ch3":ld_lds_depthch[2],
            "lds_depth_ch4":ld_lds_depthch[3],
            "lds_heat_ch1":ld_lds_heatch[0],
            "lds_heat_ch2":ld_lds_heatch[1],
            "lds_heat_ch3":ld_lds_heatch[2],
            "lds_heat_ch4":ld_lds_heatch[3],
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
            "Soilmoisture_ch9":ld_soil[8],
            "Soilmoisture_ch10":ld_soil[9],
            "Soilmoisture_ch11":ld_soil[10],
            "Soilmoisture_ch12":ld_soil[11],
            "Soilmoisture_ch13":ld_soil[12],
            "Soilmoisture_ch14":ld_soil[13],
            "Soilmoisture_ch15":ld_soil[14],
            "Soilmoisture_ch16":ld_soil[15],
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
            "devname":devname,
            "mac":mac,
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
            "Soilmoisture_ch9_batt":self.val_tobattery(ld_sen_batt[58],"","1"),
            "Soilmoisture_ch10_batt":self.val_tobattery(ld_sen_batt[59],"","1"),
            "Soilmoisture_ch11_batt":self.val_tobattery(ld_sen_batt[60],"","1"),
            "Soilmoisture_ch12_batt":self.val_tobattery(ld_sen_batt[61],"","1"),
            "Soilmoisture_ch13_batt":self.val_tobattery(ld_sen_batt[62],"","1"),
            "Soilmoisture_ch14_batt":self.val_tobattery(ld_sen_batt[63],"","1"),
            "Soilmoisture_ch15_batt":self.val_tobattery(ld_sen_batt[64],"","1"),
            "Soilmoisture_ch16_batt":self.val_tobattery(ld_sen_batt[65],"","1"),
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
            "lds_ch1_batt":self.val_tobattery(ld_sen_batt[66],"","1"),
            "lds_ch2_batt":self.val_tobattery(ld_sen_batt[67],"","1"),
            "lds_ch3_batt":self.val_tobattery(ld_sen_batt[68],"","1"),
            "lds_ch4_batt":self.val_tobattery(ld_sen_batt[69],"","1"),

        }
        # 删除值为指定字符串的键值对
        keys_to_remove = [key for key, val in list(resjson.items()) if val in ["None", "--", "", "--.-", "---.-"]]

        for key in keys_to_remove:
            del resjson[key]

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