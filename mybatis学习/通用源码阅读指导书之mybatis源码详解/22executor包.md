


# 22.9错误上下文 ErrorContext
错误上下文，将一些背景信息先保存下来，当错误真正发生错误时，就能方便得将这些背景信息提供出来，方便错误排查
* 基于线程单例ThreadLocal设计，线程单例模式，保证一个线程都有唯一的一个错误上下文
* 错误链设计,ErrorContext对象内部还有一个stored对象保存原有的ErrorContext

基本属性属性
```
private ErrorContext stored;
  private String resource;
  private String activity;
  private String object;
  private String message;
  private String sql;
  private Throwable cause;
```
设置属性方法
sql
resource
等等


操作方法
instance：获取ErrorContext的单例静态方法，获取当前线程绑定的ErrorContext,如果没有则创建一个新的ErrorContext
store：存入一个新ErrorContext
recall：剥离当前ErrorContext出来,获取上一个ErrorContext
reset：重置ErrorContext信息

ExceptionFactory的wrapException方法显示更新了ErrorContext对象的message属性和cause属性
