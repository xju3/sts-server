import requests
import os
from dotenv import load_dotenv

load_dotenv()

# api_key = os.getenv("DEEPSEEK_API_KEY")

api_key = 'Iiri0OIyQuXR6RWB1dJwFNjOHtGY/b0k47kP2sDjiEp99HECZf/h7NODJD/hqpxr'

import requests

# 你的 API 密钥

# API 端点
upload_url = 'https://chat.deepseek.com/api/v0/file/upload_file'
# upload_url = 'https://api.deepseek.com/v1/upload'
ask_url = 'https://api.deepseek.com/v1/ask'


import os

cookies = {
    'smidV2': '202501081457527c6239e20c774a7f8e9c1b397f2edfaf0035c0e162198c6c0',
    'intercom-device-id-guh50jw4': '4f5c762b-d3f0-4b7b-b8ec-127cd5209f1f',
    '.thumbcache_6b2e5483f9d858d7c661c5e276b6a6ae': 'a/w7daEIBKlTAn9s3fj+/nui+85W0twUs1IBnqT0KnpJQjvkaHqekigsXfMHeRlyq9OdO5QZ9ZKCGyOjM7N6ig%3D%3D',
    'cf_clearance': 'iuCxPoXUCXi9SDqqVP67ofvgDLMRLxOmQ8rdSswspPE-1738551253-1.2.1.1-JzNIWiJa7ZVyv8EePpyJua_cnDLrfcKZz6Niez40hsyoy_stU7DJ8ZwTNyouREsNmWabBA5YUV1UlcqSidYnxEQp0gvRpOvxZlruV_QE7RcqSTrF72.FBeXABTCnmwyktWbYxN2ImFUW7acU7LaikcDdTREvGNgIrEzsgAE5PsIsRZgQ7ocLCiDZUfHZndmMBc9k_zx7.7p4Lh_Ro0q7jfbmWeMyjlxDwmLo1wMXTrqV95YqfumJoW_NvY1IaEyk2d.9CHnfMAs_QGdESqgfZMhRAtX2cOzK4gww5P7MvXe.4Ou9i0ArXvCMMdObBeics3X7vDFp3ROmOtkYK0LtYQ',
    'Hm_lvt_1fff341d7a963a4043e858ef0e19a17c': '1738551248,1738644960,1738723232,1738854568',
    'Hm_lvt_fb5acee01d9182aabb2b61eb816d24ff': '1738634169,1738723229,1738853372,1738988471',
    'Hm_lpvt_fb5acee01d9182aabb2b61eb816d24ff': '1738988471',
    'HMACCOUNT': '728C86462C40D3AC',
    'HWWAFSESTIME': '1738988741236',
    'HWWAFSESID': '634e7b86ec037f4ac28',
    'ds_session_id': 'a64d93b927cd4e86a6398bc4e84fb2c9',
    'intercom-session-guh50jw4': 'QVpGS0VKMTloc0c1SGxLdXYzQWt5VHd2U3MyMEVLbEFDOFZUTlFtanV4cVJZTmVaSUx0Y1I1MnBQOGErRTZ6UHk4N2JkUkNRSzRGdi9RVklmK2luRVBQeis3WU05S1h4S0xJMS9ja0ZVSE09LS1iVlFCZzlxNFZhbHI3QXgxNlhWeFNRPT0=--9f0bb19d96c86f5440577f3529f5ced2d01e446e',
}


def get_file_list(directory):
    """
    获取指定目录下所有文件的路径列表。

    Args:
        directory (str): 目录路径。

    Returns:
        list: 文件路径列表。
    """
    file_list = []
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_list.append(file_path)
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    except NotADirectoryError:
        print(f"Error: '{directory}' is not a directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return file_list


# 要上传的文件路径列表
file_paths = get_file_list("/Users/tju/Workspace/projects/sts/server/files/uploads")
# 保存文件标识符
file_ids = []

# 设置请求头
headers = {
    'Authorization': f'Bearer {api_key}',
    'Referer': 'https://chat.deepseek.com/a/chat/s/7c3be685-f6a1-4348-9ecd-6ba7bd28b612'
}

# 逐个上传文件
for file_path in file_paths:
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(upload_url, headers=headers, files=files, cookies=cookies)
        
        if response.status_code == 200:
            print(f'文件 {file_path} 上传成功，file_id: {file_path}')
            print(response.json())

        else:
            print(f'文件 {file_path} 上传失败。')
            print('状态码:', response.status_code)
            print('错误信息:', response.text)
