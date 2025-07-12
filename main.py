import requests

def process_links(input_file, output_file):
    headers = {
        'accept': '*/*',
        'connection': 'Keep-Alive',
        'user-agent': 'okhttp/4.12.0',
        # 'Host': 'dd.rihou.cc:555',
        'Accept-Encoding': 'gzip',
    }

    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
@@ -9,7 +17,7 @@ def process_links(input_file, output_file):
                continue  # 跳过空行和注释行
            print(f"Fetching: {line}")
            try:
                resp = requests.get(line, headers=headers, timeout=15)
                resp.raise_for_status()
                content = resp.text.replace(' ', '\n')
                fout.write(f'# From: {line}\n')
