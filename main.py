import http.client

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            print(f"Fetching: {line}")
            try:
                # 只支持 http
                if not line.startswith("http://"):
                    raise Exception("只支持 http 链接")
                # 解析主机和路径
                url = line[len("http://"):]
                host, path = url.split("/", 1)
                path = "/" + path

                conn = http.client.HTTPConnection(host, timeout=15)
                conn.putrequest("GET", path)
                conn.putheader("accept", "*/*")
                conn.putheader("connection", "Keep-Alive")
                conn.putheader("user-agent", "okhttp/3.15")
                conn.putheader("Host", host)
                conn.endheaders()
                resp = conn.getresponse()
                status = resp.status
                content = resp.read().decode('utf-8', errors='replace')
                if status != 200:
                    raise Exception(f"HTTP {status}")
                fout.write(f'# From: {line}\n')
                fout.write(content + '\n\n')
                print(f"Fetched and wrote content from {line}")
                conn.close()
            except Exception as e:
                print(f"Failed to fetch {line}: {e}")
                fout.write(f"# Failed to fetch {line}: {e}\n\n")

if __name__ == '__main__':
    process_links('list.txt', 'output.txt')
