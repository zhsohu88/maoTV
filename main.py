import http.client
from urllib.parse import urlparse

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            print(f"Fetching: {line}")
            try:
                o = urlparse(line)
                host = o.hostname
                path = o.path
                if o.query:
                    path += '?' + o.query
                conn = http.client.HTTPConnection(host, timeout=15)
                conn.putrequest("GET", path)
                conn.putheader("accept", "*/*")
                conn.putheader("connection", "Keep-Alive")
                conn.putheader("user-agent", "okhttp/3.15")
                # 不手动加 Host 头
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
