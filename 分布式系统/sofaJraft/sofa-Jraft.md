
# 性能优化
* batch处理
* pipeline 模式

[](https://codeantenna.com/a/XBcBNtEYGb)

# jraft-example count示例项目启动
example运行示例
* 启动CounterServer 三台服务组成raft group

program argument
```
/tmp/jraft/server1 counter 127.0.0.1:8081 127.0.0.1:8081,127.0.0.1:8082,127.0.0.1:8083
/tmp/jraft/server2 counter 127.0.0.1:8082 127.0.0.1:8081,127.0.0.1:8082,127.0.0.1:8083
/tmp/jraft/server3 counter 127.0.0.1:8083 127.0.0.1:8081,127.0.0.1:8082,127.0.0.1:8083
```

启动 CounterClient
CounterClient
program argument
```
counter 127.0.0.1:8081,127.0.0.1:8082,127.0.0.1:8083
```
[Counter 例子详解](https://www.sofastack.tech/projects/sofa-jraft/counter-example/)

# 资料
## 官网

## 博客
[蚂蚁金服开源 SOFAJRaft：生产级 Java Raft 算法库](https://www.toutiao.com/i6668454178215428621/?app=news_article&group_id=6668454178215428621&is_new_connect=0&is_new_user=0&req_id=202202080756290101330511380B4F970F&share_token=9ddf6235-8fe1-40f8-823a-aa34cf303c6f&timestamp=1644278189&tt_from=weixin&use_new_style=1&utm_campaign=client_share&utm_medium=toutiao_android&utm_source=weixin&wxshare_count=1)
提到了jraft对raft算法的一些性能优化点