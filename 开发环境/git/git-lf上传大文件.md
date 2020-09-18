# 介绍
Git LFS 是 Github 开发的一个 Git 的扩展，用于实现 Git 对大文件的支持

# 资料


# 常见问题
## git push网上推的时候总是提示connection refused
```
✘ chujun@chujundeMacBook-Pro  ~/my/project/gitBackupConfig   master  git push
Uploading LFS objects:   0% (0/1), 76 MB | 959 KB/s, done.
Post https://lfs.github.com/chujun/gitBackupConfig/objects/be3f5b008d14221817f6452c486db02f8e8158c768e079b482262f9af7e6146e/verify: dial tcp 13.250.168.23:443: connect: connection refused
error: failed to push some refs to 'git@github.com:chujun/gitBackupConfig.git'
```
一般排除了网络和代理问题之外,试试git push origin master
![git lfs push解决方案](img/git-lfs%20push%20connection%20refused.png)
```
 chujun@chujundeMacBook-Pro  ~/my/project/gitBackupConfig   master  git push -u origin master
Uploading LFS objects:   0% (0/1), 0 B | 0 B/s
Uploading LFS objects: 100% (1/1), 76 MB | 502 KB/s, done.
Enumerating objects: 14, done.
Counting objects: 100% (14/14), done.
Delta compression using up to 4 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 171.31 KiB | 631.00 KiB/s, done.
Total 8 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To github.com:chujun/gitBackupConfig.git
   12ee18f..49778ff  master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
```