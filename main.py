import requests
from urllib.parse import quote

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # 跳过空行和注释行
            print(f"Fetching: {line}")
            try:
                # 中文域名转 punycode
                if '://' in line:
                    scheme, rest = line.split('://', 1)
                    host, *path_parts = rest.split('/', 1)
                    try:
                        host = host.encode('idna').decode('ascii')
                    except Exception:
                        pass
                    rest = '/'.join(path_parts) if path_parts else ''
                    url = f"{scheme}://{host}/{rest}" if rest else f"{scheme}://{host}"
                else:
                    url = line

                # 参数编码（仅对 b= 参数尝试编码）
                if 'b=' in url:
                    parts = url.split('b=')
                    pre = parts[0]
                    post = parts[1]
                    post_encoded = quote(post, safe='')  # 编码参数
                    url = pre + 'b=' + post_encoded

                headers = {
                    "accept": "*/*",
                    "connection": "Keep-Alive",
                    "user-agent": "okhttp/3.15",
                    "Host": "tv.nxog.top",
                    "Accept-Encoding": "gzip"
                }

                resp = requests.get(url, headers=headers, timeout=15)
                resp.raise_for_status()
                content = resp.text.replace(' ', '\n')
                fout.write(f'# From: {line}\n')
                fout.write(content + '\n\n')
                print(f"Fetched and wrote content from {line}")
            except Exception as e:
                print(f"Failed to fetch {line}: {e}")
                fout.write(f"# Failed to fetch {line}: {e}\n\n")

if __name__ == '__main__':
    process_links('list.txt', 'output.txt')
