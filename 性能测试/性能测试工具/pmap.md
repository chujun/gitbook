
使用系统命令pmap -x 3516查看进程的内存映射情况，会发现大量的64MB内存块存在；
统计了下，大概有50多个65404+132=65536,正好是64MB，算起来大约3个多G

[pmap -x内存映射情况](https://upload-images.jianshu.io/upload_images/13897885-f6fbc16175c8506a?imageMogr2/auto-orient/strip|imageView2/2/w/640/format/webp)