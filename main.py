import socket

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            print(f"Fetching: {line}")
            try:
                # 解析URL
                if not line.startswith("http://"):
                    raise Exception("只支持 http 链接")
                url = line[len("http://"):]
                host, path = url.split("/", 1)
                path = "/" + path

                # 构造原始HTTP请求
                request = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"accept: */*\r\n"
                    f"connection: Keep-Alive\r\n"
                    f"user-agent: okhttp/3.15\r\n"
                    f"\r\n"
                )

                # 发送请求
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(15)
                s.connect((host, 80))
                s.sendall(request.encode('utf-8'))

                response = b""
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    response += data
                s.close()

                # 解析HTTP响应
                response_text = response.decode('utf-8', errors='replace')
                header_end = response_text.find('\r\n\r\n')
                if header_end == -1:
                    raise Exception("无效HTTP响应")
                headers = response_text[:header_end]
                content = response_text[header_end+4:]

                # 检查状态码
                status_line = headers.splitlines()[0]
                if "200" not in status_line:
                    raise Exception(status_line)

                fout.write(f'# From: {line}\n')
                fout.write(content + '\n\n')
                print(f"Fetched and wrote content from {line}")
            except Exception as e:
                print(f"Failed to fetch {line}: {e}")
                fout.write(f"# Failed to fetch {line}: {e}\n\n")

if __name__ == '__main__':
    process_links('list.txt', 'output.txt')
