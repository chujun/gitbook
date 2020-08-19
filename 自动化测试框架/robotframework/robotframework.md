# 第三方库列表
## http
* requests robotframework-requests依赖该库
* RequestsLibrary 封装HTTP关键字
* HttpLibraryHTTP 可以使用该库的JSON关键字
* 其他
```bash
#requests安装
pip3 install requests
#安装指定版本
pip3 install requests==1.8.0
#RequestsLibrary安装
pip3 install robotframework-requests
#HttpLibraryHTTP安装
pip3 install robotframework-httplibrary

```


# 常见问题列表
* RobotFramework编码乱码问题，无法正确处理utf8编码
解决方案：直接编辑源代码，从ASCII支持UTF8编码方式
源码路径
```bash
/usr/local/lib/python3.8/site-packages/robot/utils/unic.py
```
两段内容
```
if PY2:

    def _unic(item):
        if isinstance(item, unicode):
            return item
        if isinstance(item, (bytes, bytearray)):
            try:
                return item.decode('ASCII')
            except UnicodeError:
                return u''.join(chr(b) if b < 128 else '\\x%x' % b
                                for b in bytearray(item))
        # fixed chinese show question start
        if isinstance(item, (list, dict,tuple)):
        	try:
        		item = json.dumps(item,ensure_ascii=False,encoding='utf-8')
        	except UnicodeDecodeError:
        		try:
        			item = json.dumps(item, ensure_ascii=False,encoding='utf-8')
        		except:
        			pass
        	except:
        		pass
       	# fixed chinese show question end
        try:
            try:
                return unicode(item)
            except UnicodeError:
                return unic(str(item))
        except:
            return _unrepresentable_object(item)

else:

    def _unic(item):
        if isinstance(item, str):
            return item
        if isinstance(item, (bytes, bytearray)):
            try:
                return item.decode('ASCII')
            except UnicodeError:
            	# fixed chinese show question start
            	try:
            		return item.decode('utf-8')
            	except UnicodeError:
                	return ''.join(chr(b) if b < 128 else '\\x%x' % b
                            	for b in item)
                # fixed chinese show question end
        try:
            return str(item)
        except:
            return _unrepresentable_object(item)

```
具体调整内容见文件
![unic.py](py/unic.py)