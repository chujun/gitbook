# __*__ coding:utf-8 __*__
# @Author:chujun
import os
import os.path

exclude_paths = ['__pycache__', 'lib', 'script', '.idea', '_book', 'node_modules', 'img', 'README.md']
level_max_limit = 3
file_name = 'SUMMARY.md'


def generate_summary_md(dir_name):
    file_prefix = generate_file_header()
    content = generate_dir_content(dir_name, [], 1)
    total = file_prefix + content
    print(total)
    generate_new_file(total, file_name)


def generate_new_file(content, file_name):
    with open(file_name, 'w+') as new_file:
        new_file.writelines(content)


def generate_file_header():
    return '''# Summary
    
* [介绍](README.md)
    
'''


def generate_dir_content(dir_name, sub_paths, level):
    if level > level_max_limit:
        return ''
    content = ''
    for x in os.listdir(dir_name):
        is_dir = os.path.isdir(os.path.join(dir_name, x))
        if level == 1 and not is_dir:
            # 最顶层不输出文件
            continue
        if level == level_max_limit and is_dir:
            # 最底层不输出目录
            continue
        if not x.startswith('.') and x not in exclude_paths:
            dir_item_content = ''
            for tab in range(1, level):
                dir_item_content += '\t'
            sub_path = ''
            for path in sub_paths:
                sub_path += path + '/'
            md = x
            if is_dir:
                md = os.path.join(x, 'README.md')
            dir_item_content += '* [%s](%s%s)\n' % (x, sub_path, md)
            content += dir_item_content
            if is_dir:
                print(x)
                copy_sub_path = copy_array_add_item(sub_paths, x)
                content += generate_dir_content(os.path.join(dir_name, x), copy_sub_path, level + 1)
            if level == 1:
                content += '---\n'
    return content


def copy_array_add_item(array, data):
    result = []
    for item in array:
        result.append(item)
    result.append(data)
    return result


if __name__ == '__main__':
    log_path = os.path.dirname(os.path.abspath(__file__))
    print(log_path)
    generate_summary_md(log_path)
