import requests

def main():
    url = "http://tv.nxog.top/m/111.php?ou=%E5%85%AC%E4%BC%97%E5%8F%B7%E6%AC%A7%E6%AD%8C"
    headers = {
        "accept": "*/*",
        "connection": "Keep-Alive",
        "user-agent": "okhttp/3.15",
        "Host": "tv.nxog.top"
        # 不加 Accept-Encoding
    }

    # 用 requests 发送请求，保持 headers 和易语言一致
    response = requests.get(url, headers=headers, timeout=15)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    main()
