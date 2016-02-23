##Xss服务端代码，简易实现##


### 如何使用

1. 运行环境  
	python2.7   
	Flask  `pip install flask`    
	
2. 运行服务	`python xss.py`
3. 访问生成xss [http://127.0.0.1/g.js](http://127.0.0.1/g.js)
	
### 函数
1. 生成xss 服务端js 

```python
	def genjs(url,id):    
		....
		...
		return js
```
