import requests

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty and comment lines
            print(f"Fetching: {line}")
            try:
                resp = requests.get(line, timeout=15)
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
