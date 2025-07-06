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
                if not line.startswith("http://"):
                    raise Exception("只支持 http 链接")
                url = line[len("http://"):]
                host, path = url.split("/", 1)
                path = "/" + path

                request = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"accept: */*\r\n"
                    f"connection: Keep-Alive\r\n"
                    f"user-agent: MTV\r\n"
                    f"Accept-Encoding: gzip\r\n"
                    f"\r\n"
                )

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

                # 保存原始响应内容
                with open('raw_response.txt', 'wb') as rawf:
                    rawf.write(response)

                # 打印原始响应内容（十六进制和文本，便于分析）
                print("======= 原始响应内容（十六进制） =======")
                print(response.hex(" ", 1))
                print("======= 原始响应内容（文本） =======")
                try:
                    print(response.decode('utf-8', errors='replace'))
                except Exception:
                    print("无法以UTF-8解码原始响应内容")

                response_text = response.decode('utf-8', errors='replace')
                header_end = response_text.find('\r\n\r\n')
                if header_end == -1:
                    # 写下原始响应供排查
                    fout.write(f"# From: {line}\n")
                    fout.write("# 未检测到有效HTTP头，原始响应如下：\n")
                    fout.write(response_text + '\n\n')
                    print(f"Failed to fetch {line}: 未检测到有效HTTP头，原始响应已保存到 raw_response.txt")
                    continue

                headers = response_text[:header_end]
                content = response_text[header_end+4:]

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
