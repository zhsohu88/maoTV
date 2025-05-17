# main.py

def process_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # 跳过空行和注释行
            # 处理链接内容，将空格替换为换行符
            output = line.replace(' ', '\n')
            fout.write(output + '\n')

if __name__ == '__main__':
    process_links('list.txt', 'output.txt')
