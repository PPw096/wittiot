"""Define an object to interact with the REST API."""
from ast import For
import asyncio
from datetime import date
import enum
from http.client import SWITCHING_PROTOCOLS
import logging
from typing import Any, Dict, List,Union, Optional, cast

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
GW11268_API_IOTINFO = "get_iot_device_list"
GW11268_API_READIOT = "parse_quick_cmd_iot"

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

TYPE_PIEZO_SR = "srain_piezo"
TYPE_PIEZO__BATT = "batt_piezo"

TYPE_CONSOLE_BATT  = "con_batt"
TYPE_CONSOLE_BVOLT = "con_batt_volt"
TYPE_CONSOLE_EVOLT = "con_ext_volt"

TYPE_PM25CH1 = "pm25_ch1"
TYPE_PM25CH2 = "pm25_ch2"
TYPE_PM25CH3 = "pm25_ch3"
TYPE_PM25CH4 = "pm25_ch4"
TYPE_PM2524HCH1 = "pm25_24h_ch1"
TYPE_PM2524HCH2 = "pm25_24h_ch2"
TYPE_PM2524HCH3 = "pm25_24h_ch3"
TYPE_PM2524HCH4 = "pm25_24h_ch4"
TYPE_PM25RTAQICH1 = "pm25_aqi_ch1"
TYPE_PM25RTAQICH2 = "pm25_aqi_ch2"
TYPE_PM25RTAQICH3 = "pm25_aqi_ch3"
TYPE_PM25RTAQICH4 = "pm25_aqi_ch4"
TYPE_PM2524HAQICH1 = "pm25_avg_24h_ch1"
TYPE_PM2524HAQICH2 = "pm25_avg_24h_ch2"
TYPE_PM2524HAQICH3 = "pm25_avg_24h_ch3"
TYPE_PM2524HAQICH4 = "pm25_avg_24h_ch4"

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

TYPE_CO2PM1 = "pm1_co2"
TYPE_CO224HPM1 = "pm1_24h_co2"
TYPE_CO2RTPM1 = "pm1_aqi_co2"
TYPE_CO2PM4 = "pm4_co2"
TYPE_CO224HPM4 = "pm4_24h_co2"
TYPE_CO2RTPM4 = "pm4_aqi_co2"

TYPE_CO2IN = "co2in"
TYPE_CO224HIN = "co2in_24h"


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
TYPE_LDSDEPCH1 = "lds_depth_ch1"
TYPE_LDSDEPCH2 = "lds_depth_ch2"
TYPE_LDSDEPCH3 = "lds_depth_ch3"
TYPE_LDSDEPCH4 = "lds_depth_ch4"
TYPE_LDSHEIGHTCH1 = "lds_height_ch1"
TYPE_LDSHEIGHTCH2 = "lds_height_ch2"
TYPE_LDSHEIGHTCH3 = "lds_height_ch3"
TYPE_LDSHEIGHTCH4 = "lds_height_ch4"
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

TYPE_WH85_BATT = "wh85_batt"
TYPE_WH90_BATT = "wh90_batt"
TYPE_WH69_BATT = "wh69_batt"
TYPE_WH68_BATT = "wh68_batt"
TYPE_WH40_BATT = "wh40_batt"
TYPE_WN20_BATT = "wn20_batt"
TYPE_WH25_BATT = "wh25_batt"
TYPE_WH26_BATT = "wh26_batt"
TYPE_WH80_BATT = "wh80_batt"
TYPE_WH57_BATT = "wh57_batt"
TYPE_WH45_BATT = "wh45_batt"


TYPE_PM25CH1_SIGNAL = "pm25_ch1_signal"
TYPE_PM25CH2_SIGNAL = "pm25_ch2_signal"
TYPE_PM25CH3_SIGNAL = "pm25_ch3_signal"
TYPE_PM25CH4_SIGNAL = "pm25_ch4_signal"
TYPE_LEAKCH1_SIGNAL = "leak_ch1_signal"
TYPE_LEAKCH2_SIGNAL = "leak_ch2_signal"
TYPE_LEAKCH3_SIGNAL = "leak_ch3_signal"
TYPE_LEAKCH4_SIGNAL = "leak_ch4_signal"
TYPE_TEMPCH1_SIGNAL = "temph_ch1_signal"
TYPE_TEMPCH2_SIGNAL = "temph_ch2_signal"
TYPE_TEMPCH3_SIGNAL = "temph_ch3_signal"
TYPE_TEMPCH4_SIGNAL = "temph_ch4_signal"
TYPE_TEMPCH5_SIGNAL = "temph_ch5_signal"
TYPE_TEMPCH6_SIGNAL = "temph_ch6_signal"
TYPE_TEMPCH7_SIGNAL = "temph_ch7_signal"
TYPE_TEMPCH8_SIGNAL = "temph_ch8_signal"
TYPE_SOILCH1_SIGNAL = "Soilmoisture_ch1_signal"
TYPE_SOILCH2_SIGNAL = "Soilmoisture_ch2_signal"
TYPE_SOILCH3_SIGNAL = "Soilmoisture_ch3_signal"
TYPE_SOILCH4_SIGNAL = "Soilmoisture_ch4_signal"
TYPE_SOILCH5_SIGNAL = "Soilmoisture_ch5_signal"
TYPE_SOILCH6_SIGNAL = "Soilmoisture_ch6_signal"
TYPE_SOILCH7_SIGNAL = "Soilmoisture_ch7_signal"
TYPE_SOILCH8_SIGNAL = "Soilmoisture_ch8_signal"
TYPE_SOILCH9_SIGNAL = "Soilmoisture_ch9_signal"
TYPE_SOILCH10_SIGNAL = "Soilmoisture_ch10_signal"
TYPE_SOILCH11_SIGNAL = "Soilmoisture_ch11_signal"
TYPE_SOILCH12_SIGNAL = "Soilmoisture_ch12_signal"
TYPE_SOILCH13_SIGNAL = "Soilmoisture_ch13_signal"
TYPE_SOILCH14_SIGNAL = "Soilmoisture_ch14_signal"
TYPE_SOILCH15_SIGNAL = "Soilmoisture_ch15_signal"
TYPE_SOILCH16_SIGNAL = "Soilmoisture_ch16_signal"
TYPE_ONLYTEMPCH1_SIGNAL = "tf_ch1_signal"
TYPE_ONLYTEMPCH2_SIGNAL = "tf_ch2_signal"
TYPE_ONLYTEMPCH3_SIGNAL = "tf_ch3_signal"
TYPE_ONLYTEMPCH4_SIGNAL = "tf_ch4_signal"
TYPE_ONLYTEMPCH5_SIGNAL = "tf_ch5_signal"
TYPE_ONLYTEMPCH6_SIGNAL = "tf_ch6_signal"
TYPE_ONLYTEMPCH7_SIGNAL = "tf_ch7_signal"
TYPE_ONLYTEMPCH8_SIGNAL = "tf_ch8_signal"
TYPE_LEAFCH1_SIGNAL = "leaf_ch1_signal"
TYPE_LEAFCH2_SIGNAL = "leaf_ch2_signal"
TYPE_LEAFCH3_SIGNAL = "leaf_ch3_signal"
TYPE_LEAFCH4_SIGNAL = "leaf_ch4_signal"
TYPE_LEAFCH5_SIGNAL = "leaf_ch5_signal"
TYPE_LEAFCH6_SIGNAL = "leaf_ch6_signal"
TYPE_LEAFCH7_SIGNAL = "leaf_ch7_signal"
TYPE_LEAFCH8_SIGNAL = "leaf_ch8_signal"
TYPE_LDSCH1_SIGNAL = "lds_ch1_signal"
TYPE_LDSCH2_SIGNAL = "lds_ch2_signal"
TYPE_LDSCH3_SIGNAL = "lds_ch3_signal"
TYPE_LDSCH4_SIGNAL = "lds_ch4_signal"
TYPE_WH85_SIGNAL = "wh85_signal"
TYPE_WH90_SIGNAL = "wh90_signal"
TYPE_WH69_SIGNAL = "wh69_signal"
TYPE_WH68_SIGNAL = "wh68_signal"
TYPE_WH40_SIGNAL = "wh40_signal"
TYPE_WN20_SIGNAL = "wn20_signal"
TYPE_WH25_SIGNAL = "wh25_signal"
TYPE_WH26_SIGNAL = "wh26_signal"
TYPE_WH80_SIGNAL = "wh80_signal"
TYPE_WH57_SIGNAL = "wh57_signal"
TYPE_WH45_SIGNAL = "wh45_signal"

TYPE_PM25CH1_RSSI = "pm25_ch1_rssi"
TYPE_PM25CH2_RSSI = "pm25_ch2_rssi"
TYPE_PM25CH3_RSSI = "pm25_ch3_rssi"
TYPE_PM25CH4_RSSI = "pm25_ch4_rssi"
TYPE_LEAKCH1_RSSI = "leak_ch1_rssi"
TYPE_LEAKCH2_RSSI = "leak_ch2_rssi"
TYPE_LEAKCH3_RSSI = "leak_ch3_rssi"
TYPE_LEAKCH4_RSSI = "leak_ch4_rssi"
TYPE_TEMPCH1_RSSI = "temph_ch1_rssi"
TYPE_TEMPCH2_RSSI = "temph_ch2_rssi"
TYPE_TEMPCH3_RSSI = "temph_ch3_rssi"
TYPE_TEMPCH4_RSSI = "temph_ch4_rssi"
TYPE_TEMPCH5_RSSI = "temph_ch5_rssi"
TYPE_TEMPCH6_RSSI = "temph_ch6_rssi"
TYPE_TEMPCH7_RSSI = "temph_ch7_rssi"
TYPE_TEMPCH8_RSSI = "temph_ch8_rssi"
TYPE_SOILCH1_RSSI = "Soilmoisture_ch1_rssi"
TYPE_SOILCH2_RSSI = "Soilmoisture_ch2_rssi"
TYPE_SOILCH3_RSSI = "Soilmoisture_ch3_rssi"
TYPE_SOILCH4_RSSI = "Soilmoisture_ch4_rssi"
TYPE_SOILCH5_RSSI = "Soilmoisture_ch5_rssi"
TYPE_SOILCH6_RSSI = "Soilmoisture_ch6_rssi"
TYPE_SOILCH7_RSSI = "Soilmoisture_ch7_rssi"
TYPE_SOILCH8_RSSI = "Soilmoisture_ch8_rssi"
TYPE_SOILCH9_RSSI = "Soilmoisture_ch9_rssi"
TYPE_SOILCH10_RSSI = "Soilmoisture_ch10_rssi"
TYPE_SOILCH11_RSSI = "Soilmoisture_ch11_rssi"
TYPE_SOILCH12_RSSI = "Soilmoisture_ch12_rssi"
TYPE_SOILCH13_RSSI = "Soilmoisture_ch13_rssi"
TYPE_SOILCH14_RSSI = "Soilmoisture_ch14_rssi"
TYPE_SOILCH15_RSSI = "Soilmoisture_ch15_rssi"
TYPE_SOILCH16_RSSI = "Soilmoisture_ch16_rssi"
TYPE_ONLYTEMPCH1_RSSI = "tf_ch1_rssi"
TYPE_ONLYTEMPCH2_RSSI = "tf_ch2_rssi"
TYPE_ONLYTEMPCH3_RSSI = "tf_ch3_rssi"
TYPE_ONLYTEMPCH4_RSSI = "tf_ch4_rssi"
TYPE_ONLYTEMPCH5_RSSI = "tf_ch5_rssi"
TYPE_ONLYTEMPCH6_RSSI = "tf_ch6_rssi"
TYPE_ONLYTEMPCH7_RSSI = "tf_ch7_rssi"
TYPE_ONLYTEMPCH8_RSSI = "tf_ch8_rssi"
TYPE_LEAFCH1_RSSI = "leaf_ch1_rssi"
TYPE_LEAFCH2_RSSI = "leaf_ch2_rssi"
TYPE_LEAFCH3_RSSI = "leaf_ch3_rssi"
TYPE_LEAFCH4_RSSI = "leaf_ch4_rssi"
TYPE_LEAFCH5_RSSI = "leaf_ch5_rssi"
TYPE_LEAFCH6_RSSI = "leaf_ch6_rssi"
TYPE_LEAFCH7_RSSI = "leaf_ch7_rssi"
TYPE_LEAFCH8_RSSI = "leaf_ch8_rssi"
TYPE_LDSCH1_RSSI = "lds_ch1_rssi"
TYPE_LDSCH2_RSSI = "lds_ch2_rssi"
TYPE_LDSCH3_RSSI = "lds_ch3_rssi"
TYPE_LDSCH4_RSSI = "lds_ch4_rssi"

TYPE_WH85_RSSI = "wh85_rssi"
TYPE_WH90_RSSI = "wh90_rssi"
TYPE_WH69_RSSI = "wh69_rssi"
TYPE_WH68_RSSI = "wh68_rssi"
TYPE_WH40_RSSI = "wh40_rssi"
TYPE_WN20_RSSI = "wn20_rssi"
TYPE_WH25_RSSI = "wh25_rssi"
TYPE_WH26_RSSI = "wh26_rssi"
TYPE_WH80_RSSI = "wh80_rssi"
TYPE_WH57_RSSI = "wh57_rssi"
TYPE_WH45_RSSI = "wh45_rssi"

iotMap = {
		   1: 'WFC01',
		   2: 'AC1100',
		   3: 'WFC02',
}
runMap = {
	    'WFC01': 'water_running',
		'WFC02': 'water_running',
		'AC1100': 'ac_running',
 }
formatDataMap = {
			    'WFC01': ['happen_water', 'water_total', 'flow_velocity', 'water_action', 'water_temp'],
			    'WFC02': ['happen_water', 'wfc02_total', 'wfc02_flow_velocity', 'water_action', 'water_temp'],
			    'AC1100': ['happen_elect', 'elect_total', 'realtime_power', 'ac_action', 'ac_voltage'],
}
wfcMap = {
		  'WFC01': ['rssi', 'flow_velocity', 'water_status', 'water_total', 'wfc01batt', ],
		  'WFC02': ['wfc02rssi', 'wfc02_flow_velocity', 'wfc02_status', 'wfc02_total', 'wfc02batt', ],
		  'AC1100': ['rssi']
}

class SubSensorname:
    prefixes = [
        "Haptic 3-in-1",
        "Haptic Array",
        "Sensor Array",
        "Wind Sensor",
        "Rainfall Sensor",
        "Rain Gauge Mini",
        "T&RH&P Sensor",
        "Outdoor T&RH Sensor",
        "Sonic Array",
        "Lightning Sensor",
        "AQI Combo Sensor",
        "CH1 PM25",
        "CH2 PM25",
        "CH3 PM25",
        "CH4 PM25",
        "CH1 LEAK",
        "CH2 LEAK",
        "CH3 LEAK",
        "CH4 LEAK",
        "CH1 T&H",
        "CH2 T&H",
        "CH3 T&H",
        "CH4 T&H",
        "CH5 T&H",
        "CH6 T&H",
        "CH7 T&H",
        "CH8 T&H",
        "CH1 Soil",
        "CH2 Soil",
        "CH3 Soil",
        "CH4 Soil",
        "CH5 Soil",
        "CH6 Soil",
        "CH7 Soil",
        "CH8 Soil",
        "CH9 Soil",
        "CH10 Soil",
        "CH11 Soil",
        "CH12 Soil",
        "CH13 Soil",
        "CH14 Soil",
        "CH15 Soil",
        "CH16 Soil",
        "CH1 Temp",
        "CH2 Temp",
        "CH3 Temp",
        "CH4 Temp",
        "CH5 Temp",
        "CH6 Temp",
        "CH7 Temp",
        "CH8 Temp",
        "CH1 Leaf",
        "CH2 Leaf",
        "CH3 Leaf",
        "CH4 Leaf",
        "CH5 Leaf",
        "CH6 Leaf",
        "CH7 Leaf",
        "CH8 Leaf",
        "CH1 Lds",
        "CH2 Lds",
        "CH3 Lds",
        "CH4 Lds",
    ]

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
    BATTERY_BINARY=9
    SIGNAL = 10
    RSSI = 11



class MultiSensorInfo:
    """Multi Sensor Info."""

    SENSOR_INFO={
        TYPE_PM25CH1 : {"dev_type": "CH1 PM25","name":"CH1 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25CH2 : {"dev_type": "CH2 PM25","name":"CH2 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25CH3 : {"dev_type": "CH3 PM25","name":"CH3 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM25CH4 : {"dev_type": "CH4 PM25","name":"CH4 PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM2524HCH1 : {"dev_type": "CH1 PM25","name":"CH1 24H Avg PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM2524HCH2 : {"dev_type": "CH2 PM25","name":"CH2 24H Avg PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM2524HCH3 : {"dev_type": "CH3 PM25","name":"CH3 24H Avg PM2.5","data_type":WittiotDataTypes.PM25},
        TYPE_PM2524HCH4 : {"dev_type": "CH4 PM25","name":"CH4 24H Avg PM2.5","data_type":WittiotDataTypes.PM25},
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
        TYPE_LDSHEIGHTCH1 : {"dev_type": "CH1 Lds","name":"CH1 Total Height","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSHEIGHTCH2 : {"dev_type": "CH2 Lds","name":"CH2 Total Height","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSHEIGHTCH3 : {"dev_type": "CH3 Lds","name":"CH3 Total Height","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSHEIGHTCH4 : {"dev_type": "CH4 Lds","name":"CH4 Total Height","data_type":WittiotDataTypes.DISTANCE},
        TYPE_LDSHEATCH1 : {"dev_type": "CH1 Lds","name":"CH1 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_LDSHEATCH2 : {"dev_type": "CH2 Lds","name":"CH2 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_LDSHEATCH3 : {"dev_type": "CH3 Lds","name":"CH3 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        TYPE_LDSHEATCH4 : {"dev_type": "CH4 Lds","name":"CH4 Heater-on Counter","data_type":WittiotDataTypes.HEAT},
        
        TYPE_PM25CH1_SIGNAL : {"dev_type": "CH1 PM25","name":"CH1 PM2.5 Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_PM25CH2_SIGNAL : {"dev_type": "CH2 PM25","name":"CH2 PM2.5 Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_PM25CH3_SIGNAL : {"dev_type": "CH3 PM25","name":"CH3 PM2.5 Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_PM25CH4_SIGNAL : {"dev_type": "CH4 PM25","name":"CH4 PM2.5 Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAKCH1_SIGNAL : {"dev_type": "CH1 LEAK","name":"CH1 LEAK Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAKCH2_SIGNAL : {"dev_type": "CH2 LEAK","name":"CH2 LEAK Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAKCH3_SIGNAL : {"dev_type": "CH3 LEAK","name":"CH3 LEAK Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAKCH4_SIGNAL : {"dev_type": "CH4 LEAK","name":"CH4 LEAK Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH1_SIGNAL : {"dev_type": "CH1 T&H","name":"CH1 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH2_SIGNAL : {"dev_type": "CH2 T&H","name":"CH2 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH3_SIGNAL : {"dev_type": "CH3 T&H","name":"CH3 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH4_SIGNAL : {"dev_type": "CH4 T&H","name":"CH4 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH5_SIGNAL : {"dev_type": "CH5 T&H","name":"CH5 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH6_SIGNAL : {"dev_type": "CH6 T&H","name":"CH6 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH7_SIGNAL : {"dev_type": "CH7 T&H","name":"CH7 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_TEMPCH8_SIGNAL : {"dev_type": "CH8 T&H","name":"CH8 T&H Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH1_SIGNAL : {"dev_type": "CH1 Soil","name":"CH1 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH2_SIGNAL : {"dev_type": "CH2 Soil","name":"CH2 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH3_SIGNAL : {"dev_type": "CH3 Soil","name":"CH3 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH4_SIGNAL : {"dev_type": "CH4 Soil","name":"CH4 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH5_SIGNAL : {"dev_type": "CH5 Soil","name":"CH5 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH6_SIGNAL : {"dev_type": "CH6 Soil","name":"CH6 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH7_SIGNAL : {"dev_type": "CH7 Soil","name":"CH7 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH8_SIGNAL : {"dev_type": "CH8 Soil","name":"CH8 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH9_SIGNAL : {"dev_type": "CH9 Soil","name":"CH9 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH10_SIGNAL : {"dev_type": "CH10 Soil","name":"CH10 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH11_SIGNAL : {"dev_type": "CH11 Soil","name":"CH11 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH12_SIGNAL : {"dev_type": "CH12 Soil","name":"CH12 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH13_SIGNAL : {"dev_type": "CH13 Soil","name":"CH13 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH14_SIGNAL : {"dev_type": "CH14 Soil","name":"CH14 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH15_SIGNAL : {"dev_type": "CH15 Soil","name":"CH15 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_SOILCH16_SIGNAL : {"dev_type": "CH16 Soil","name":"CH16 Soil Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH1_SIGNAL : {"dev_type": "CH1 Temp","name":"CH1 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH2_SIGNAL : {"dev_type": "CH2 Temp","name":"CH2 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH3_SIGNAL : {"dev_type": "CH3 Temp","name":"CH3 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH4_SIGNAL : {"dev_type": "CH4 Temp","name":"CH4 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH5_SIGNAL : {"dev_type": "CH5 Temp","name":"CH5 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH6_SIGNAL : {"dev_type": "CH6 Temp","name":"CH6 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH7_SIGNAL : {"dev_type": "CH7 Temp","name":"CH7 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_ONLYTEMPCH8_SIGNAL : {"dev_type": "CH8 Temp","name":"CH8 Temp Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH1_SIGNAL : {"dev_type": "CH1 Leaf","name":"CH1 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH2_SIGNAL : {"dev_type": "CH2 Leaf","name":"CH2 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH3_SIGNAL : {"dev_type": "CH3 Leaf","name":"CH3 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH4_SIGNAL : {"dev_type": "CH4 Leaf","name":"CH4 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH5_SIGNAL : {"dev_type": "CH5 Leaf","name":"CH5 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH6_SIGNAL : {"dev_type": "CH6 Leaf","name":"CH6 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH7_SIGNAL : {"dev_type": "CH7 Leaf","name":"CH7 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LEAFCH8_SIGNAL : {"dev_type": "CH8 Leaf","name":"CH8 Leaf Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LDSCH1_SIGNAL : {"dev_type": "CH1 Lds","name":"CH1 Lds Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LDSCH2_SIGNAL : {"dev_type": "CH2 Lds","name":"CH2 Lds Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LDSCH3_SIGNAL : {"dev_type": "CH3 Lds","name":"CH3 Lds Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_LDSCH4_SIGNAL : {"dev_type": "CH4 Lds","name":"CH4 Lds Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH85_SIGNAL : {"dev_type": "Haptic 3-in-1","name":"Haptic 3-in-1 Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH90_SIGNAL : {"dev_type": "Haptic Array","name":"Haptic Array Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH69_SIGNAL : {"dev_type": "Sensor Array","name":"Sensor Array Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH68_SIGNAL : {"dev_type": "Wind Sensor","name":"Wind Sensor Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH40_SIGNAL : {"dev_type": "Rainfall Sensor","name":"Rainfall Sensor Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WN20_SIGNAL : {"dev_type": "Rain Gauge Mini","name":"Rain Gauge Mini Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH25_SIGNAL : {"dev_type": "T&RH&P Sensor","name":"T&RH&P Sensor Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH26_SIGNAL : {"dev_type": "Outdoor T&RH Sensor","name":"Outdoor T&RH Sensor Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH80_SIGNAL : {"dev_type": "Sonic Array","name":"Sonic Array Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH57_SIGNAL : {"dev_type": "Lightning Sensor","name":"Lightning Sensor Signal","data_type":WittiotDataTypes.SIGNAL},
        TYPE_WH45_SIGNAL : {"dev_type": "AQI Combo Sensor","name":"AQI Combo Sensor Signal","data_type":WittiotDataTypes.SIGNAL},
        
        TYPE_PM25CH1_RSSI : {"dev_type": "CH1 PM25","name":"CH1 PM2.5 Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_PM25CH2_RSSI : {"dev_type": "CH2 PM25","name":"CH2 PM2.5 Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_PM25CH3_RSSI : {"dev_type": "CH3 PM25","name":"CH3 PM2.5 Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_PM25CH4_RSSI : {"dev_type": "CH4 PM25","name":"CH4 PM2.5 Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAKCH1_RSSI : {"dev_type": "CH1 LEAK","name":"CH1 LEAK Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAKCH2_RSSI : {"dev_type": "CH2 LEAK","name":"CH2 LEAK Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAKCH3_RSSI : {"dev_type": "CH3 LEAK","name":"CH3 LEAK Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAKCH4_RSSI : {"dev_type": "CH4 LEAK","name":"CH4 LEAK Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH1_RSSI : {"dev_type": "CH1 T&H","name":"CH1 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH2_RSSI : {"dev_type": "CH2 T&H","name":"CH2 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH3_RSSI : {"dev_type": "CH3 T&H","name":"CH3 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH4_RSSI : {"dev_type": "CH4 T&H","name":"CH4 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH5_RSSI : {"dev_type": "CH5 T&H","name":"CH5 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH6_RSSI : {"dev_type": "CH6 T&H","name":"CH6 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH7_RSSI : {"dev_type": "CH7 T&H","name":"CH7 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_TEMPCH8_RSSI : {"dev_type": "CH8 T&H","name":"CH8 T&H Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH1_RSSI : {"dev_type": "CH1 Soil","name":"CH1 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH2_RSSI : {"dev_type": "CH2 Soil","name":"CH2 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH3_RSSI : {"dev_type": "CH3 Soil","name":"CH3 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH4_RSSI : {"dev_type": "CH4 Soil","name":"CH4 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH5_RSSI : {"dev_type": "CH5 Soil","name":"CH5 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH6_RSSI : {"dev_type": "CH6 Soil","name":"CH6 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH7_RSSI : {"dev_type": "CH7 Soil","name":"CH7 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH8_RSSI : {"dev_type": "CH8 Soil","name":"CH8 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH9_RSSI : {"dev_type": "CH9 Soil","name":"CH9 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH10_RSSI : {"dev_type": "CH10 Soil","name":"CH10 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH11_RSSI : {"dev_type": "CH11 Soil","name":"CH11 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH12_RSSI : {"dev_type": "CH12 Soil","name":"CH12 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH13_RSSI : {"dev_type": "CH13 Soil","name":"CH13 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH14_RSSI : {"dev_type": "CH14 Soil","name":"CH14 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH15_RSSI : {"dev_type": "CH15 Soil","name":"CH15 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_SOILCH16_RSSI : {"dev_type": "CH16 Soil","name":"CH16 Soil Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH1_RSSI : {"dev_type": "CH1 Temp","name":"CH1 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH2_RSSI : {"dev_type": "CH2 Temp","name":"CH2 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH3_RSSI : {"dev_type": "CH3 Temp","name":"CH3 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH4_RSSI : {"dev_type": "CH4 Temp","name":"CH4 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH5_RSSI : {"dev_type": "CH5 Temp","name":"CH5 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH6_RSSI : {"dev_type": "CH6 Temp","name":"CH6 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH7_RSSI : {"dev_type": "CH7 Temp","name":"CH7 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_ONLYTEMPCH8_RSSI : {"dev_type": "CH8 Temp","name":"CH8 Temp Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH1_RSSI : {"dev_type": "CH1 Leaf","name":"CH1 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH2_RSSI : {"dev_type": "CH2 Leaf","name":"CH2 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH3_RSSI : {"dev_type": "CH3 Leaf","name":"CH3 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH4_RSSI : {"dev_type": "CH4 Leaf","name":"CH4 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH5_RSSI : {"dev_type": "CH5 Leaf","name":"CH5 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH6_RSSI : {"dev_type": "CH6 Leaf","name":"CH6 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH7_RSSI : {"dev_type": "CH7 Leaf","name":"CH7 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LEAFCH8_RSSI : {"dev_type": "CH8 Leaf","name":"CH8 Leaf Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LDSCH1_RSSI : {"dev_type": "CH1 Lds","name":"CH1 Lds Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LDSCH2_RSSI : {"dev_type": "CH2 Lds","name":"CH2 Lds Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LDSCH3_RSSI : {"dev_type": "CH3 Lds","name":"CH3 Lds Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_LDSCH4_RSSI : {"dev_type": "CH4 Lds","name":"CH4 Lds Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH85_RSSI : {"dev_type": "Haptic 3-in-1","name":"Haptic 3-in-1 Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH90_RSSI : {"dev_type": "Haptic Array","name":"Haptic Array Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH69_RSSI : {"dev_type": "Sensor Array","name":"Sensor Array Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH68_RSSI : {"dev_type": "Wind Sensor","name":"Wind Sensor Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH40_RSSI : {"dev_type": "Rainfall Sensor","name":"Rainfall Sensor Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WN20_RSSI : {"dev_type": "Rain Gauge Mini","name":"Rain Gauge Mini Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH25_RSSI : {"dev_type": "T&RH&P Sensor","name":"T&RH&P Sensor Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH26_RSSI : {"dev_type": "Outdoor T&RH Sensor","name":"Outdoor T&RH Sensor Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH80_RSSI : {"dev_type": "Sonic Array","name":"Sonic Array Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH57_RSSI : {"dev_type": "Lightning Sensor","name":"Lightning Sensor Rssi","data_type":WittiotDataTypes.RSSI},
        TYPE_WH45_RSSI : {"dev_type": "AQI Combo Sensor","name":"AQI Combo Sensor Rssi","data_type":WittiotDataTypes.RSSI},
        
        TYPE_PM25CH1_BATT : {"dev_type": "CH1 PM25","name":"CH1 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_PM25CH2_BATT : {"dev_type": "CH2 PM25","name":"CH2 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_PM25CH3_BATT : {"dev_type": "CH3 PM25","name":"CH3 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_PM25CH4_BATT : {"dev_type": "CH4 PM25","name":"CH4 PM2.5 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH1_BATT : {"dev_type": "CH1 LEAK","name":"CH1 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH2_BATT : {"dev_type": "CH2 LEAK","name":"CH2 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH3_BATT : {"dev_type": "CH3 LEAK","name":"CH3 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_LEAKCH4_BATT : {"dev_type": "CH4 LEAK","name":"CH4 LEAK Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_TEMPCH1_BATT : {"dev_type": "CH1 T&H","name":"CH1 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH2_BATT : {"dev_type": "CH2 T&H","name":"CH2 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH3_BATT : {"dev_type": "CH3 T&H","name":"CH3 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH4_BATT : {"dev_type": "CH4 T&H","name":"CH4 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH5_BATT : {"dev_type": "CH5 T&H","name":"CH5 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH6_BATT : {"dev_type": "CH6 T&H","name":"CH6 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH7_BATT : {"dev_type": "CH7 T&H","name":"CH7 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
        TYPE_TEMPCH8_BATT : {"dev_type": "CH8 T&H","name":"CH8 T&H Battery","data_type":WittiotDataTypes.BATTERY_BINARY},
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
        TYPE_WH85_BATT : {"dev_type": "Haptic 3-in-1","name":"Haptic 3-in-1 Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH90_BATT : {"dev_type": "Haptic Array","name":"Haptic Array Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH69_BATT : {"dev_type": "Sensor Array","name":"Sensor Array Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH68_BATT : {"dev_type": "Wind Sensor","name":"Wind Sensor Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH40_BATT : {"dev_type": "Rainfall Sensor","name":"Rainfall Sensor Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WN20_BATT : {"dev_type": "Rain Gauge Mini","name":"Rain Gauge Mini Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH25_BATT : {"dev_type": "T&RH&P Sensor","name":"T&RH&P Sensor Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH26_BATT : {"dev_type": "Outdoor T&RH Sensor","name":"Outdoor T&RH Sensor Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH80_BATT : {"dev_type": "Sonic Array","name":"Sonic Array Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH57_BATT : {"dev_type": "Lightning Sensor","name":"Lightning Sensor Battery","data_type":WittiotDataTypes.BATTERY},
        TYPE_WH45_BATT : {"dev_type": "AQI Combo Sensor","name":"AQI Combo Sensor Battery","data_type":WittiotDataTypes.BATTERY},
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
        
        self.unit_temp = 0


    def is_valid_float(self,val):
        try:
            float(val)  # 尝试转换 
            return True 
        except (ValueError, TypeError):  # 捕获无效转换 
            return False 
    async def _request_data(
        self, 
        url: str,
        ignore_errors: tuple = (404, 405)
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
        # 先检查接口是否可用
        
        try:
            async with session.request("get", url) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                # print(data)
        except ClientError as err:
            # print(err)
            # 检查错误状态码是否在忽略列表中
            if hasattr(err, 'status') and err.status in ignore_errors:
                self._logger.debug("Endpoint not available (ignored): %s, Error: %s", url, err)
                return []
            raise RequestError(f"Error requesting data from {url}: {err}") from err
        finally:
            if not use_running_session:
                await session.close()
        self._logger.debug("_request_data Received data for %s: %s", url, data)
        return cast(List[Dict[str, Any]], data)
    async def is_endpoint_available(self, url: str) -> bool:
        """检查设备接口是否可用"""
        use_running_session = self._session and not self._session.closed
        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.head(url) as resp:
                return resp.status == 200
        finally:
            if not use_running_session:
                await session.close()
    async def _post_data(
        self, 
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Make a POST request against the API."""
        use_running_session = self._session and not self._session.closed
        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))
        assert session

        # 打印调试信息（与GET方法保持相同风格）
        self._logger.debug("POST Request to %s", url)
        self._logger.debug("POST Payload: %s", payload)
        self._logger.debug("POST Params: %s", params)

        try:
            # 准备请求参数
            request_kwargs = {}
            if payload:
                request_kwargs["json"] = payload
            if params:
                request_kwargs["params"] = params

            # 发送POST请求
            async with session.request("POST", url, **request_kwargs) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                self._logger.debug("POST Response from %s: %s", url, data)
                return data

        except ClientError as err:
            error_msg = f"Error POSTing data to {url}: {err}"
            self._logger.error(error_msg, exc_info=True)
            raise RequestError(error_msg) from err

        finally:
            # 会话关闭逻辑保持相同
            if not use_running_session:
                await session.close()

    async def update_single_device(self, 
        command: Dict[str, Dict[str, Any]] = None,):
        
        # 直接访问command列表
        if command is None or len(command) == 0:
            return None
        
        commands = command['command']
        for i,item in enumerate(commands):
            # if item["rfnet_state"] == 0:
            #     continue
            cmd = {
                "cmd": "read_device",
                "id": item["id"],
                "model": item["model"]
            }
            payload = {"command": [cmd]}
            try:
                url = f"http://{self._ip}/{GW11268_API_READIOT}"
                response = await self._post_data(
                    url,  # 替换为实际API端点
                    payload=payload
                )
                # 3. 处理响应并更新设备状态
                response=self.extract_device_data(response,item["rfnet_state"])
                if response:
                # 方法1: 直接更新原始项
                    commands[i].update(response)
            except Exception as err:
                # 错误处理
                self._logger.debug(f"更新设备状态失败: {err}")
        return commands
        
    async def switch_iotdevice(self,_iot_id,_iot_model,_iot_switch):
        # {"command":[{"on_type":0,"off_type":0,"always_on":1,"on_time":0,"off_time":0,"val_type":1,"val":0,"cmd":"quick_run","id":1753,"model":1}]}
        # {"command":[{"cmd":"quick_stop","id":1753,"model":1}]}
        if _iot_switch == 0:
            cmd = {
                    "cmd": "quick_stop",
                    "id": _iot_id,
                    "model": _iot_model
            }
        else:
            if _iot_model == 3:
                cmd = {
                    "position":100,
                    "always_on":1,
                    "val_type":1,
                    "val":0,
                    "cmd":"quick_run",
                    "id": _iot_id,
                    "model": _iot_model
                }
            else:
                cmd = {
                    "on_type":0,
                    "off_type":0,
                    "always_on":1,
                    "on_time":0,
                    "off_time":0,
                    "val_type":1,
                    "val":0,
                    "cmd":"quick_run",
                    "id": _iot_id,
                    "model": _iot_model
                }
        payload = {"command": [cmd]}
        response = None
        try:
            url = f"http://{self._ip}/{GW11268_API_READIOT}"
            response = await self._post_data(
                url,  # 替换为实际API端点
                payload=payload
            )
        except Exception as err:
            # 错误处理
            self._logger.debug(f"更新设备状态失败: {err}")
        return response
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
    async def _request_loc_iotlist(self) -> List[Dict[str, Any]]:
        url = f"http://{self._ip}/{GW11268_API_IOTINFO}"
        val=await self._request_data(url)
        return val
    # self.extract_device_data(val)
    
    

    def locval_totemp(self,val,unit):
        if val=="" or val =="--" or val =="--.-":
            return val
        if self.is_valid_float(val):
            val=float(val)
        else:
             return ""
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
        if self.is_valid_float(val):
            val=float(val)
        else:
             return ""
        if unit=="0":
            val=round(val/304.8,2)
        else:
            val
        return val
    def locval_tohumi(self,val):
        val=val.replace("%","")
        return val
    def locval_tosrain(self,val):
        if val=="" or val =="--" or val =="--.-":
            return val
        if val=="0":
            val="No rain"
        else:
            val="Raining"
        return val
    def val_tobattery(self,val,unit,nty):
        if val=="" or val =="--" or val =="--.-":
            return val
        if nty=="0":
            if unit!="":
                val=f"{val} {unit}"
            else:
                if self.is_valid_float(val):
                    val=float(val)
                else:
                     return ""
                val=int(val)
                if val>0 and val<=5:
                    val=f"{val*20}%"
                elif val==6:
                    val="DC"
                else:
                    val=""
        elif nty=="1":
            if self.is_valid_float(val):
                val=float(val)
            else:
                return ""
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
        if self.is_valid_float(val):
            val=float(val)
        else:
            return ""
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
        if self.is_valid_float(val):
            val=float(val)
        else:
            return ""
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
        if self.is_valid_float(val):
            val=float(val)
        else:
            return ""
        if unit=="0":
            val=round((val/ 25.4),2)
        return val
    def locval_tosr(self,val,unit):
        if val=="" or val =="--" or val =="--.-" or val =="---.-":
            return val
        val=val.replace("W/m2","")
        val=val.replace("Kfc","")
        val=val.replace("Klux","")
        if self.is_valid_float(val):
            val=float(val)
        else:
            return ""
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
        if self.is_valid_float(val):
            val=float(val)
        else:
            return ""
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
        if self.is_valid_float(val):
            val=float(val)
        else:
            return ""
        if unit=="0":
            val=round(( val* 0.62137 ),1)
        elif unit=="1":
            val=round(( val* 0.62137 ),1)
        elif unit=="2":
            val
        else:
            val=round(( val / 0.53996 * 0.62137 ),1)
        return val
    def val_tobattery_binary(self,val,ld_tempch,ld_humich):
        if val=="" or val =="--" or val =="--.-":
            return val
        if ld_tempch in ["None", "--", "", "--.-", "---.-" "--.--"] and ld_humich in ["None", "--", "", "--.-", "---.-" "--.--"] :
            return "--"
        if val=="0":
            val="Normal"
        else:
            val="Low"
        return val
    def val_tobattery_binary_mk2(self,val):
        if val=="" or val =="--" or val =="--.-":
            return val
        if val=="0":
            val="Normal"
        else:
            val="Low"
        return val
    def extract_device_data(self,response,val) -> dict[int, dict]:
        """
        从 API 响应中提取设备数据
        :param response: API 返回的原始响应字典
        :return: 以设备ID为键的字典包含设备数据
        """
        
        # 1. 验证响应结构
        if "command" not in response:
            return None

        # 2. 提取设备列表
        devices = response["command"]
        res= response["command"][0]
        # print(res)
        
        iotType=""
        isWFC=""
        nickname=""
        rssi=""
        iotbatt=""
        publish_time=""
        iot_always_on=""
        data_rate=""
        run_time=""
        data_total=""
        iot_action=""
        iot_running=""
        data_val_type=""
        data_water=""
        data_ac=""
        wfc02_position=""
        
        device_info = {}
        
        if val == 0: 
            nickname=res["nickname"]
            device_info["nickname"]=nickname
        else:
            iotType = iotMap[res["model"]]
            isWFC = res["model"] != 2
            nickname=res["nickname"]
            device_info["nickname"]=nickname
            rssi=res[wfcMap[iotType][0]]
            device_info["rssi"]=rssi
            iotbatt= res[wfcMap[iotType][4]] if isWFC else  ''
            iotbatt=self.val_tobattery(iotbatt,"","1")
            device_info["iotbatt"]=iotbatt
            publish_time=res["publish_time"]
            iot_always_on=res["always_on"]
            data_rate=res[formatDataMap[iotType][2]]
            device_info[formatDataMap[iotType][2]]=data_rate
            run_time=res["run_time"]
            device_info["run_time"]=run_time
            data_total=float(res[formatDataMap[iotType][1]])-float(res[formatDataMap[iotType][0]])
            iot_action=res[formatDataMap[iotType][3]]
            iot_running=res[runMap[iotType]]
            device_info["iot_running"]=iot_running
            data_val_type=res["val_type"]
            run_time=res["run_time"]
            device_info["run_time"]=run_time
            if isWFC:
                if formatDataMap[iotType][4] in res:
                    data_water = res[formatDataMap[iotType][4]]
                    device_info["data_water_t"]=self.locval_totemp(data_water,self.unit_temp)
                if iotType == "WFC02":
                    wfc02_position=res["wfc02_position"]
                    device_info["wfc02_position"]=wfc02_position
                device_info["velocity_total"]=data_total
                if res["val_type"]==3:
                    data_val=round(res["val"]/10.0,1)
                else:
                    data_val=res["val"]
            else:
                data_ac=res[formatDataMap[iotType][4]]
                device_info["data_ac_v"]=data_ac
                device_info["elect_total"]=data_total

        keys_to_remove = [key for key, val in list(device_info.items()) if val in ["None", "--","---", "----", "", "--.-", "---.-", "--.--",None, []]]

        for key in keys_to_remove:
            del device_info[key]

        return device_info
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
        piezora_state= ''	
        piezora_batt= ''

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
        ld_pm2524hch1= ''
        ld_pm2524hch2= ''
        ld_pm2524hch3= ''
        ld_pm2524hch4= ''
        
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
        ld_lds_height=[]
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
        
        ld_co2_pm1= ''
        ld_co2_pm124= ''
        ld_co2_pm1_AQI=''
        ld_co2_pm4= ''
        ld_co2_pm424= ''
        ld_co2_pm4_AQI=''
        ld_co2_pm1_24 =''
        ld_co2_pm4_24 =''
        ld_co2_pm25_24=''
        ld_co2_pm10_24=''
        
        ld_con_batt= ''
        ld_con_batt_volt= ''
        ld_con_ext_volt= ''


        ld_sen_batt=[]
        ld_sen_rssi  =[]
        ld_sen_signal=[]
        # url = f"http://{self._ip}/{GW11268_API_UNIT}"
        res_data = await self._request_loc_data()
        res_info = await self._request_loc_info()
        res_unit = await self._request_loc_unit()
        res_batt1 = await self._request_loc_batt1()
        res_batt2 = await self._request_loc_batt2()
        res_sys = await self._request_loc_sys()
        res_mac = await self._request_loc_mac()
        
        unit_temp =res_unit["temperature"]
        unit_press=res_unit["pressure"]
        unit_wind =res_unit["wind"]
        unit_rain =res_unit["rain"]
        unit_light=res_unit["light"]
        
        self.unit_temp = unit_temp 


        res_iotlist = await self._request_loc_iotlist()
        
        res_iotdata =  await self.update_single_device(res_iotlist)
        
        # print(res_iotdata )
        # print(res_info )
        # print(res_unit )
        # print(res_batt1 )
        # print(res_batt2 )

        

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
                    piezora_batt=res_data["piezoRain"][index].get("battery", "--")
                elif res_data["piezoRain"][index]["id"]=='0x14':
                    piezora_total=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='0x7C':
                    piezora_24hour=res_data["piezoRain"][index]["val"]
                elif res_data["piezoRain"][index]["id"]=='srain_piezo':
                    piezora_state=res_data["piezoRain"][index]["val"]

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
            
        if "console" in res_data:
            ld_con_batt     =res_data["console"][0].get("battery", "--")
            ld_con_batt_volt=res_data["console"][0].get("console_batt_volt", "--")
            ld_con_ext_volt  =res_data["console"][0].get("console_ext_volt", "--")

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
             ld_co2_pm1= res_data["co2"][0].get("PM1", "--")
             ld_co2_pm124= res_data["co2"][0].get("PM1_24HAQI", "--")
             ld_co2_pm1_AQI=res_data["co2"][0].get("PM1_RealAQI", "--")
             ld_co2_pm4= res_data["co2"][0].get("PM4", "--")
             ld_co2_pm424= res_data["co2"][0].get("PM4_24HAQI", "--")
             ld_co2_pm4_AQI=res_data["co2"][0].get("PM4_RealAQI", "--")
             ld_co2_pm1_24 =res_data["co2"][0].get("PM1_24H", "--")
             ld_co2_pm4_24 =res_data["co2"][0].get("PM4_24H", "--")
             ld_co2_pm25_24=res_data["co2"][0].get("PM25_24H", "--")
             ld_co2_pm10_24=res_data["co2"][0].get("PM10_24H", "--")

        if "ch_pm25" in res_data:
            for index in range(len(res_data["ch_pm25"])):
                if res_data["ch_pm25"][index]["channel"]=='1':
                    ld_pm25ch1=res_data["ch_pm25"][index]["PM25"]
                    ld_pm2524hch1=res_data["ch_pm25"][index].get("PM25_24H", "--")
                    ld_pm25ch1_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch1_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                elif res_data["ch_pm25"][index]["channel"]=='2':
                    ld_pm25ch2=res_data["ch_pm25"][index]["PM25"]
                    ld_pm2524hch2=res_data["ch_pm25"][index].get("PM25_24H", "--")
                    ld_pm25ch2_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch2_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                elif res_data["ch_pm25"][index]["channel"]=='3':
                    ld_pm25ch3=res_data["ch_pm25"][index]["PM25"]
                    ld_pm2524hch3=res_data["ch_pm25"][index].get("PM25_24H", "--")
                    ld_pm25ch3_AQI=res_data["ch_pm25"][index]["PM25_RealAQI"]
                    ld_pm25ch3_24AQI=res_data["ch_pm25"][index]["PM25_24HAQI"]
                elif res_data["ch_pm25"][index]["channel"]=='4':
                    ld_pm25ch4=res_data["ch_pm25"][index]["PM25"]
                    ld_pm2524hch4=res_data["ch_pm25"][index].get("PM25_24H", "--")
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
        ld_lds_height=[]
        for i in range(16):
            ld_soil.append("--")
            ld_tempch.append("--")
            ld_humich.append("--")
            ld_onlytempch.append("--")
            ld_leafch.append("--")
            ld_lds_airch.append("--")
            ld_lds_depthch.append("--")
            ld_lds_heatch.append("--")
            ld_lds_height.append("--")

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
                ld_lds_height[ch]=self.locval_tolds(res_data["ch_lds"][index].get("total_height", "--"),unit_rain)

        ld_sen_batt=[]
        ld_sen_rssi  =[]
        ld_sen_signal=[]
        for i in range(99):
            ld_sen_batt.append("--")
            ld_sen_rssi.append("--")
            ld_sen_signal.append("--")


        for index in range(len(res_batt1)):
            ch=int(res_batt1[index]["type"])
            if res_batt1[index]["id"] == "FFFFFFFF" or res_batt1[index]["id"] == "FFFFFFFE":
                ld_sen_batt[ch]  ="--"
                ld_sen_rssi[ch]  ="--"
                ld_sen_signal[ch]="--"
            else:
                ld_sen_batt[ch]  =res_batt1[index]["batt"]
                ld_sen_rssi[ch]  =res_batt1[index].get("rssi", "--")
                ld_sen_signal[ch]=res_batt1[index].get("signal", "--")
           
            

        for index in range(len(res_batt2)):
            ch=int(res_batt2[index]["type"])
            if res_batt2[index]["id"] == "FFFFFFFF" or res_batt2[index]["id"] == "FFFFFFFE":
                ld_sen_batt[ch]  ="--"
                ld_sen_rssi[ch]  ="--"
                ld_sen_signal[ch]="--"
            else:
                ld_sen_batt[ch]  =res_batt2[index]["batt"]
                ld_sen_rssi[ch]  =res_batt2[index].get("rssi", "--")
                ld_sen_signal[ch]=res_batt2[index].get("signal", "--")


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
            "srain_piezo":self.locval_tosrain(piezora_state),
            "piezora_batt":self.val_tobattery(piezora_batt,"","1"),
            "con_batt":self.val_tobattery(ld_con_batt,"","1"),    
            "con_batt_volt":ld_con_batt_volt,  
            "con_ext_volt" :ld_con_ext_volt,  
            "pm25_ch1":ld_pm25ch1,
            "pm25_ch2":ld_pm25ch2,
            "pm25_ch3":ld_pm25ch3,
            "pm25_ch4":ld_pm25ch4,
            "pm25_24h_ch1":ld_pm2524hch1,
            "pm25_24h_ch2":ld_pm2524hch2,
            "pm25_24h_ch3":ld_pm2524hch3,
            "pm25_24h_ch4":ld_pm2524hch4,
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
            "pm1_co2":ld_co2_pm1,
            "pm1_24h_co2":ld_co2_pm124,
            "pm1_aqi_co2":ld_co2_pm1_AQI,
            "pm4_co2":ld_co2_pm4,
            "pm4_24h_co2":ld_co2_pm424,
            "pm4_aqi_co2":ld_co2_pm4_AQI,
            "pm1_24h_co2_add":ld_co2_pm1_24,
            "pm4_24h_co2_add":ld_co2_pm4_24,
            "pm25_24h_co2_add":ld_co2_pm25_24,
            "pm10_24h_co2_add":ld_co2_pm10_24,
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
            "lds_height_ch1":ld_lds_height[0],
            "lds_height_ch2":ld_lds_height[1],
            "lds_height_ch3":ld_lds_height[2],
            "lds_height_ch4":ld_lds_height[3],
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
            
            "pm25_ch1_rssi":ld_sen_rssi[22],
            "pm25_ch2_rssi":ld_sen_rssi[23],
            "pm25_ch3_rssi":ld_sen_rssi[24],
            "pm25_ch4_rssi":ld_sen_rssi[25],
            "leak_ch1_rssi":ld_sen_rssi[27],
            "leak_ch2_rssi":ld_sen_rssi[28],
            "leak_ch3_rssi":ld_sen_rssi[29],
            "leak_ch4_rssi":ld_sen_rssi[30],
            "temph_ch1_rssi":ld_sen_rssi[6],
            "temph_ch2_rssi":ld_sen_rssi[7],
            "temph_ch3_rssi":ld_sen_rssi[8],
            "temph_ch4_rssi":ld_sen_rssi[9],
            "temph_ch5_rssi":ld_sen_rssi[10],
            "temph_ch6_rssi":ld_sen_rssi[11],
            "temph_ch7_rssi":ld_sen_rssi[12],
            "temph_ch8_rssi":ld_sen_rssi[13],
            "Soilmoisture_ch1_rssi":ld_sen_rssi[14],
            "Soilmoisture_ch2_rssi":ld_sen_rssi[15],
            "Soilmoisture_ch3_rssi":ld_sen_rssi[16],
            "Soilmoisture_ch4_rssi":ld_sen_rssi[17],
            "Soilmoisture_ch5_rssi":ld_sen_rssi[18],
            "Soilmoisture_ch6_rssi":ld_sen_rssi[19],
            "Soilmoisture_ch7_rssi":ld_sen_rssi[20],
            "Soilmoisture_ch8_rssi":ld_sen_rssi[21],
            "Soilmoisture_ch9_rssi":ld_sen_rssi[58],
            "Soilmoisture_ch10_rssi":ld_sen_rssi[59],
            "Soilmoisture_ch11_rssi":ld_sen_rssi[60],
            "Soilmoisture_ch12_rssi":ld_sen_rssi[61],
            "Soilmoisture_ch13_rssi":ld_sen_rssi[62],
            "Soilmoisture_ch14_rssi":ld_sen_rssi[63],
            "Soilmoisture_ch15_rssi":ld_sen_rssi[64],
            "Soilmoisture_ch16_rssi":ld_sen_rssi[65],
            "tf_ch1_rssi":ld_sen_rssi[31],
            "tf_ch2_rssi":ld_sen_rssi[32],
            "tf_ch3_rssi":ld_sen_rssi[33],
            "tf_ch4_rssi":ld_sen_rssi[34],
            "tf_ch5_rssi":ld_sen_rssi[35],
            "tf_ch6_rssi":ld_sen_rssi[36],
            "tf_ch7_rssi":ld_sen_rssi[37],
            "tf_ch8_rssi":ld_sen_rssi[38],
            "leaf_ch1_rssi":ld_sen_rssi[40],
            "leaf_ch2_rssi":ld_sen_rssi[41],
            "leaf_ch3_rssi":ld_sen_rssi[42],
            "leaf_ch4_rssi":ld_sen_rssi[43],
            "leaf_ch5_rssi":ld_sen_rssi[44],
            "leaf_ch6_rssi":ld_sen_rssi[45],
            "leaf_ch7_rssi":ld_sen_rssi[46],
            "leaf_ch8_rssi":ld_sen_rssi[47],
            "lds_ch1_rssi":ld_sen_rssi[66],
            "lds_ch2_rssi":ld_sen_rssi[67],
            "lds_ch3_rssi":ld_sen_rssi[68],
            "lds_ch4_rssi":ld_sen_rssi[69],
            "wh85_rssi":ld_sen_rssi[49],
            "wh90_rssi":ld_sen_rssi[48],
            "wh69_rssi":ld_sen_rssi[0],
            "wh68_rssi":ld_sen_rssi[1],
            "wh40_rssi":ld_sen_rssi[3],
            "wn20_rssi":ld_sen_rssi[70],
            "wh25_rssi":ld_sen_rssi[4],
            "wh26_rssi":ld_sen_rssi[5],
            "wh80_rssi":ld_sen_rssi[2],
            "wh57_rssi":ld_sen_rssi[26],
            "wh45_rssi":ld_sen_rssi[39],
            "pm25_ch1_signal":ld_sen_signal[22],
            "pm25_ch2_signal":ld_sen_signal[23],
            "pm25_ch3_signal":ld_sen_signal[24],
            "pm25_ch4_signal":ld_sen_signal[25],
            "leak_ch1_signal":ld_sen_signal[27],
            "leak_ch2_signal":ld_sen_signal[28],
            "leak_ch3_signal":ld_sen_signal[29],
            "leak_ch4_signal":ld_sen_signal[30],
            "temph_ch1_signal":ld_sen_signal[6],
            "temph_ch2_signal":ld_sen_signal[7],
            "temph_ch3_signal":ld_sen_signal[8],
            "temph_ch4_signal":ld_sen_signal[9],
            "temph_ch5_signal":ld_sen_signal[10],
            "temph_ch6_signal":ld_sen_signal[11],
            "temph_ch7_signal":ld_sen_signal[12],
            "temph_ch8_signal":ld_sen_signal[13],
            "Soilmoisture_ch1_signal":ld_sen_signal[14],
            "Soilmoisture_ch2_signal":ld_sen_signal[15],
            "Soilmoisture_ch3_signal":ld_sen_signal[16],
            "Soilmoisture_ch4_signal":ld_sen_signal[17],
            "Soilmoisture_ch5_signal":ld_sen_signal[18],
            "Soilmoisture_ch6_signal":ld_sen_signal[19],
            "Soilmoisture_ch7_signal":ld_sen_signal[20],
            "Soilmoisture_ch8_signal":ld_sen_signal[21],
            "Soilmoisture_ch9_signal":ld_sen_signal[58],
            "Soilmoisture_ch10_signal":ld_sen_signal[59],
            "Soilmoisture_ch11_signal":ld_sen_signal[60],
            "Soilmoisture_ch12_signal":ld_sen_signal[61],
            "Soilmoisture_ch13_signal":ld_sen_signal[62],
            "Soilmoisture_ch14_signal":ld_sen_signal[63],
            "Soilmoisture_ch15_signal":ld_sen_signal[64],
            "Soilmoisture_ch16_signal":ld_sen_signal[65],
            "tf_ch1_signal":ld_sen_signal[31],
            "tf_ch2_signal":ld_sen_signal[32],
            "tf_ch3_signal":ld_sen_signal[33],
            "tf_ch4_signal":ld_sen_signal[34],
            "tf_ch5_signal":ld_sen_signal[35],
            "tf_ch6_signal":ld_sen_signal[36],
            "tf_ch7_signal":ld_sen_signal[37],
            "tf_ch8_signal":ld_sen_signal[38],
            "leaf_ch1_signal":ld_sen_signal[40],
            "leaf_ch2_signal":ld_sen_signal[41],
            "leaf_ch3_signal":ld_sen_signal[42],
            "leaf_ch4_signal":ld_sen_signal[43],
            "leaf_ch5_signal":ld_sen_signal[44],
            "leaf_ch6_signal":ld_sen_signal[45],
            "leaf_ch7_signal":ld_sen_signal[46],
            "leaf_ch8_signal":ld_sen_signal[47],
            "lds_ch1_signal":ld_sen_signal[66],
            "lds_ch2_signal":ld_sen_signal[67],
            "lds_ch3_signal":ld_sen_signal[68],
            "lds_ch4_signal":ld_sen_signal[69],
            "wh85_signal":ld_sen_signal[49],
            "wh90_signal":ld_sen_signal[48],
            "wh69_signal":ld_sen_signal[0],
            "wh68_signal":ld_sen_signal[1],
            "wh40_signal":ld_sen_signal[3],
            "wn20_signal":ld_sen_signal[70],
            "wh25_signal":ld_sen_signal[4],
            "wh26_signal":ld_sen_signal[5],
            "wh80_signal":ld_sen_signal[2],
            "wh57_signal":ld_sen_signal[26],
            "wh45_signal":ld_sen_signal[39],
            # "allbatt":ld_sen_batt,
            "pm25_ch1_batt":self.val_tobattery(ld_sen_batt[22],"","1"),
            "pm25_ch2_batt":self.val_tobattery(ld_sen_batt[23],"","1"),
            "pm25_ch3_batt":self.val_tobattery(ld_sen_batt[24],"","1"),
            "pm25_ch4_batt":self.val_tobattery(ld_sen_batt[25],"","1"),
            "leak_ch1_batt":self.val_tobattery(ld_sen_batt[27],"","1"),
            "leak_ch2_batt":self.val_tobattery(ld_sen_batt[28],"","1"),
            "leak_ch3_batt":self.val_tobattery(ld_sen_batt[29],"","1"),
            "leak_ch4_batt":self.val_tobattery(ld_sen_batt[30],"","1"),
            "temph_ch1_batt":self.val_tobattery_binary(ld_sen_batt[6] ,ld_tempch[0],ld_humich[0]),
            "temph_ch2_batt":self.val_tobattery_binary(ld_sen_batt[7] ,ld_tempch[1],ld_humich[1]),
            "temph_ch3_batt":self.val_tobattery_binary(ld_sen_batt[8] ,ld_tempch[2],ld_humich[2]),
            "temph_ch4_batt":self.val_tobattery_binary(ld_sen_batt[9] ,ld_tempch[3],ld_humich[3]),
            "temph_ch5_batt":self.val_tobattery_binary(ld_sen_batt[10],ld_tempch[4],ld_humich[4]),
            "temph_ch6_batt":self.val_tobattery_binary(ld_sen_batt[11],ld_tempch[5],ld_humich[5]),
            "temph_ch7_batt":self.val_tobattery_binary(ld_sen_batt[12],ld_tempch[6],ld_humich[6]),
            "temph_ch8_batt":self.val_tobattery_binary(ld_sen_batt[13],ld_tempch[7],ld_humich[7]),
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
            "wh85_batt":self.val_tobattery(ld_sen_batt[49],"","1"),
            "wh90_batt":self.val_tobattery(ld_sen_batt[48],"","1"),
            "wh69_batt":self.val_tobattery_binary_mk2(ld_sen_batt[0]),
            "wh68_batt":self.val_tobattery(ld_sen_batt[1],"","1"),
            "wh40_batt":self.val_tobattery(ld_sen_batt[3],"","1"),
            "wn20_batt":self.val_tobattery(ld_sen_batt[70],"","1"),
            "wh25_batt":self.val_tobattery_binary_mk2(ld_sen_batt[4]),
            "wh26_batt":self.val_tobattery_binary_mk2(ld_sen_batt[5]),
            "wh80_batt":self.val_tobattery(ld_sen_batt[2],"","1"),
            "wh57_batt":self.val_tobattery(ld_sen_batt[26],"","1"),
            "wh45_batt":self.val_tobattery(ld_sen_batt[39],"","1"),
            
            "iot_list": res_iotlist
        }
        # hex_str = format(255, 'X')
        # 删除值为指定字符串的键值对
        keys_to_remove = [key for key, val in list(resjson.items()) if val in ["None", "--","---", "----", "", "--.-", "---.-", "--.--",None, []]]

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