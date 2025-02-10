# -*- coding: utf-8 -*- 
import urllib.parse
import requests
import json, os
import hashlib
import urllib
from dotenv import load_dotenv


load_dotenv()
# 百度地图API密钥和SK
API_KEY = os.getenv("BAIDU_MAP_AK")
SECRET_KEY = os.getenv("BAIDU_MAP_SK")

def get_baidu_signed_url(latitude, longitude, radius):
    parameters = f"/place/v2/search?query=学校&location={latitude},{longitude}&radius={radius * 1000}&output=json&ak={API_KEY}"
    encodedStr = urllib.parse.quote(parameters, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + SECRET_KEY
    md5 = hashlib.md5(urllib.parse.quote_plus(rawStr).encode("utf-8")).hexdigest() 
    return f'http://api.map.baidu.com{encodedStr}&sn={md5}'


def baidu_get_schools_nearby(latitude, longitude, radius=5):
    """
    根据经纬度查询附近学校
    Args:
        latitude: 纬度
        longitude: 经度
        radius: 半径，单位公里

    Returns:
        学校列表，包含学校名称、地址和距离
    """

    map_url = get_baidu_signed_url(latitude, longitude, radius)
    response = requests.get(map_url)
    data = json.loads(response.text)
    results = data['results']
    if len(results) > 0:
        schools = []
        for poi in results:

            if "telephone" not in poi:
                poi["telephone"] = ""
            if "name" not in poi:
                poi["name"] = ""
            if "address" not in poi:
                poi["address"] = ""
            if "location" not in poi:
                poi["location"] = {}
            if "lat" not in poi["location"]:
                poi["location"]["lat"] = 0.0
            if "lng" not in poi["location"]:
                poi["location"]["lng"] = 0.0
            
            school = {
                "name": poi["name"],
                "address": poi["address"],
                "phone": poi["telephone"],
                "lat": poi["location"]["lat"],
                "lng": poi["location"]["lng"],
                "addr": poi["address"],
            }
            schools.append(school)
        return schools
    else:
        return []

