# 11.1背景知识
## 11.1.1XML文件
定义文档可以使用DTD(Document Type Definition，文档类型定义),也可以用Schema
![](img/eleven/11xml结构树.png)
![](img/eleven/11Schema示例.png)
![](img/eleven/11SDTD示例.png)
![](img/eleven/11mybatis%20DOCTYPE解释.png)

## 11.1.2XPath
解析xml的一种方式
![](img/eleven/11XPath语法示例.png)
![](img/eleven/11XPath%20java示例.png)

## 11.2XML解析
mybatis的parsing包是用来进行XML文件解析的包
*XPathParser*与*XNode*类是最为关键的类
![](img/eleven/11XPathParser与XNode类主要关系的类图.png)
XPathParser类内包含了XPath对象，因此具有了xml解析能力

```java
public class XPathParser {
    /**
     * 被解析的文档对象
     */
    private final Document document;
    /**
     * 是否开启验证
     */
    private boolean validation;

    /**
     * 通过EntityResolver可以申明寻找DTD文件的方法，例如通过本地寻找，而不是只能通过网络下载DTD文件
     */
    private EntityResolver entityResolver;
    /**
     * Mybatis配置文件的properties节点信息
     */
    private Properties variables;
    /**
     * XPath xml文件解析工具对象
     */
    private XPath xpath;
}
```
XPathParser具有多个重载的构造方法，还提供了XML文档中节点解析功能的"eval*"方法
最终都会调用如下方法,通过XPath解析xml文件内容
```
private Object evaluate(String expression, Object root, QName returnType) {
    try {
      //对指定节点root运行解析语法expression，获得returnType类型的解析结果
      return xpath.evaluate(expression, root, returnType);
    } catch (Exception e) {
      throw new BuilderException("Error evaluating XPath.  Cause: " + e, e);
    }
  }
```

同样的XNode类是org.w3c.dom.Node类的包装类，只是多了一些属性。

```java
/**
 * 本质上是对Node对象的包装类，多提供了一个属性
 * @author Clinton Begin
 */
public class XNode {
    //表示XML文件的一个节点
    private final Node node;
    //节点名,可以从Node中获取
    private final String name;
    //节点体,可以从Node中获取
    private final String body;
    //节点属性，可以从Node中获取
    private final Properties attributes;
    //Mybatis配置文件中的properties节点属性
    private final Properties variables;
    //XML解析器
    private final XPathParser xpathParser;
}
```
XNode类同样封装了很多"get*"和"eval*"方法,从而能够解析自身节点内的信息

# 11.3文档解析中的变量替换
Mybatis配置文件中properties节点会在解析配置文件的最开始就被解析,以供解析后续节点时发挥作用.
那么这个是如何实现的呢?







