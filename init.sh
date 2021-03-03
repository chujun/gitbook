#处理plantuml历史遗留图片
#移除多余的图片
rm -rf _book/assets

#把生成的图片批量复制到_book对应目录下
cp -R assets/ _book/assets/