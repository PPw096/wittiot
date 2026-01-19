import sys, os 
# 获取t.py 的父目录（即wittiot包路径）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,  BASE_DIR)  # 添加到模块搜索路径 
 
from wittiot.api  import API  # 改为绝对导入

import json
import logging
import math
from datetime import datetime, timedelta
#from api import API
from aiohttp import ClientSession
from tabulate import tabulate

def table_print(data: dict) -> str:
    """使用表格格式输出设备数据"""
    # 分组数据
    groups = {
        "气象数据": [],
        "空气质量": [],
        "设备信息": [],
        "电池状态": [],
        "其他传感器": []
    }
    
    # 定义每个组的键
    weather_keys = ["tempinf", "humidityin", "baromrelin", "baromabsin", "tempf", "humidity", 
                  "winddir", "windspeedmph", "windgustmph", "solarradiation", "uv", "daywindmax", 
                  "dewpoint", "rainratein", "eventrainin", "dailyrainin", "weeklyrainin", 
                  "monthlyrainin", "yearlyrainin"]
    
    air_quality_keys = ["pm25_ch1", "pm25_aqi_ch1", "pm25_avg_24h_ch1", "co2", "co2_24h", 
                     "pm25_co2", "pm25_24h_co2", "pm10_co2", "pm10_24h_co2", "pm10_aqi_co2", 
                     "pm25_aqi_co2"]
    
    device_info_keys = ["ver", "devname", "mac"]
    iot_info_keys = ["iot_list"]
    
    battery_keys = [k for k in data.keys() if "_batt" in k]
    
    # 填充组数据
    for key, value in data.items():
        if key in weather_keys:
            groups["气象数据"].append([key, value])
        elif key in air_quality_keys:
            groups["空气质量"].append([key, value])
        elif key in device_info_keys:
            groups["设备信息"].append([key, value])
        elif key in battery_keys:
            groups["电池状态"].append([key, value])
        elif key in iot_info_keys:
            print((value))
        else:
            groups["其他传感器"].append([key, value])
    
    # 创建输出
    output = []
    output.append("==== 设备数据报告 ====")
    output.append(f"设备名称: {data.get('devname', '未知设备')}")
    output.append(f"MAC地址: {data.get('mac', '未知')}")
    output.append(f"固件版本: {data.get('ver', '未知')}\n")
    
    # 添加每个组的表格
    for group, items in groups.items():
        if items:
            output.append(f"◆ {group}")
            output.append(tabulate(items, headers=["参数", "值"], tablefmt="grid"))
            output.append("")
    
    return "\n".join(output)

async def main() -> None:
    async with ClientSession() as session:
        try:
            api = API("192.168.4.1", session=session)
            res = await api._request_loc_allinfo()
            # authtoken=99be59a1bd105ed5
            # log=stdout
            # loglevel=INFO
            # 使用表格格式输出
           
            print(table_print(res))
            # date_str = "2023-07-06"  # 示例字符串 
            # yesterday = datetime.strptime(date_str,  "%Y-%m-%d")  # 转为日期对象 
            # # yesterday="2025-7-6"
            # max_temp=21.5
            # min_temp=12.3
            # max_humi=84
            # min_humi=63
            # J6=9.25
            # mean_wind=2.78
            # self_wind_height=10
            # self_altitude=100
            # self_latitude=50.48
            # u2 = mean_wind * 4.87 / math.log(67.8*self_wind_height - 5.42)

            # # Calculate yesterday's ETO
            # avg_temp = (max_temp + min_temp) / 2
            # # self._yesterday_gdd = max(0, avg_temp - self._base_temp)
            # # Calculate accumulated ETO from start date to yesterday

            # R1 = (4098 * 0.6108 * math.exp(17.27 * avg_temp / (avg_temp + 237.3))) / (
            #     avg_temp + 237.3
            # ) ** 2
            # R2 = 101.3 * ((293 - 0.0065 * self_altitude) / 293) ** 5.26
            # R3 = 0.665e-3 * R2
            # R4 = 0.6108 * math.exp(17.27 * max_temp / (max_temp + 237.3))
            # R5 = 0.6108 * math.exp(17.27 * min_temp / (min_temp + 237.3))
            # R6 = 0.5 * (R4 * min_humi / 100 + R5 * max_humi / 100)
            # R7 = 0.5 * (R4 + R5)
            # num_str = f"{self_latitude:.2f}"
            # parts = num_str.split(".")
            # integer_part = int(parts[0])
            # fractional_part = int(parts[1])
            # R8 = integer_part + (fractional_part / 60.0)
            # R9 = yesterday.timetuple().tm_yday
            # R10 = math.radians(R8)
            # R11 = 1 + 0.033 * math.cos(2 * math.pi * R9 / 365)
            # R12 = 0.409 * math.sin(2 * math.pi * R9 / 365 - 1.39)
            # R13 = math.acos(-math.tan(R10) * math.tan(R12))
            # R14 = (
            #     (24 * 60 / math.pi)
            #     * 0.082
            #     * R11
            #     * (
            #         R13 * math.sin(R10) * math.sin(R12)
            #         + math.cos(R10) * math.cos(R12) * math.sin(R13)
            #     )
            # )
            # R15 = (0.75 + 2e-5 * R8) * R14
            # R16 = 24 * R13 / math.pi
            # R17 = (0.25 + 0.5 * J6 / R16) * R14
            # R18 = 0.77 * R17
            # R19 = 273.16 + max_temp
            # R20 = 273.16 + min_temp
            # R21 = (
            #     (4.9031e-9 * (R19**4 + R20**4) / 2)
            #     * (0.34 - 0.14 * R6**0.5)
            #     * (1.35 * R17 / R15 - 0.35)
            # )
            # R22 = R18 - R21
            # R23 = 0
            # R24 = (
            #     0.408 * R1 * (R22 - R23) + R3 * 900 * u2 * (R7 - R6) / (avg_temp + 273)
            # ) / (R1 + R3 * (1 + 0.34 * u2))
            
            # for i in range(1, 25):
            #     if f"R{i}" in locals():
            #         print(f"R{i} = {locals()[f'R{i}']}")
            # # res = await api.switch_iotdevice(10311,3,0)
            # # print((res))
        except Exception as e:
            logging.error("发生错误: %s", e, exc_info=True)

if __name__ == "__main__":
    # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    import asyncio
    asyncio.run(main())