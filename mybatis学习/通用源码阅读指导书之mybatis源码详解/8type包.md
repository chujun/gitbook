type类有55个之多，比较繁杂，此时一定要注意归类总结

经过梳理，主要分为六组
类型处理器:1个接口，1个基础实现类，1个辅助类，43个实现类
TypeHandler：类型处理器接口
BaseTypeHandler:类型处理器的基础实现
TypeReference：类型参考器
-*TypeHandler:43个类型处理器

类型注册表：3个
-SimpleTypeRegistry：基本类型注册表，内部用set维护了所有java基本类型集合
-TypeAliasRegistry：类型别名注册表，内部使用hashmap维护所有类型的别名和类型的映射关系
-TypeHandlerRegistry：类型处理器注册表，内部维护所有类型和对应类型处理器的映射关系

注解类
-Alias：使用该注解可以给类设置别名，设置后，别名和类型的映射关系便存入
—MappedJdbcTypes：自定义扩展某些处理器处理某些JDBC类型，只需继承BaseTypeHandler子类，然后加上该注解，生命它要处理的JDBC类型即可
-MappedTypes：自定义扩展处理器处理某些Java类型

异常类：1ge
-TypeException：表示与类型处理相关的异常

工具类：1个
ByteArrayUtils:提供数组转化的工具方法

枚举类:1个
JdbcType

# 8.1模板模式
TODO:cj to be done