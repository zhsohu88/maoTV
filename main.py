import requests

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # 跳过空行和注释行
            print(f"Fetching: {line}")
            try:
                resp = requests.get(line, timeout=10)
                resp.raise_for_status()
                content = resp.text.replace(' ', '\n')
                fout.write(content + '\n')
                print(f"Fetched and wrote content from {line}")
            except Exception as e:
                print(f"Failed to fetch {line}: {e}")
                fout.write(f"# Failed to fetch {line}: {e}\n")

if __name__ == '__main__':
    process_links('list.txt', 'output.txt')
