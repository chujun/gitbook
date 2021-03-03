主要用来梳理下mybatis框架运行的uml

# mybatis框架运行活动图
```uml
@startuml
(*)-->用户mapper接口抽象方法
-->MapperProxy.invoke
-->MapperMethod.execute
-->MappedStatement(针对select查询语句)
@enduml
```