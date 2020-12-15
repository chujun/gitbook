# coding:utf-8
# 一键生成项目枚举的md说明文件
import os


def content(file_name):
with open(file_name) as file:
return file.read()


def generate_mark_down(dir_name):
total_content = ''
path = dir_name
for x in os.listdir(dir_name):
full_path = os.path.join('%s%s' % (dir_name, x))
print(path + x + ',' + full_path)
if os.path.isfile(full_path) and os.path.splitext(full_path)[1] == '.java':
total_content += '# {}\n```\n{}\n```\n'.format(os.path.splitext(x)[0], content(full_path))
return total_content


if __name__ == '__main__':
print("start")
#dir_name = '/Users/chujun/my/project/ahs/trade-in-center/trade-in-center-model/src/main/java/com/aihuishou/service/tic/model/enumerate/'
dir_name ='/Users/chujun/my/project/ahs/trade-in-center/trade-in-center-service/src/main/java/com/aihuishou/service/tic/enumerate/'
content = generate_mark_down(dir_name)
print(content)
with open('a.md', 'w+') as new_file:
new_file.writelines(content)