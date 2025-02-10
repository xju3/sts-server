
from  domain.manager.location_manager import baidu_get_schools_nearby
if __name__ == "__main__":
    latitude = 31.1267959
    longitude = 121.4172526

    print(baidu_get_schools_nearby(latitude, longitude, 5))