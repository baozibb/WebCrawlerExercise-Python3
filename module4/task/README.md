## task

* task1 

代理的设置方法。由于没有代理，一些东西试验不了，就随便写了点。以后有代理的时候现用现查吧。

* task4

利用 [超级鹰](https://www.chaojiying.com/) 平台，获取图像验证码的验证。

测试网站：https://captcha3.scrape.cuiqingcai.com/

刚开始，有时候成功有时候失败，有点迷，我还以为代码逻辑有问题，后来发现，超级鹰的验证码类型设置错了，坑死

1-4 个变长坐标的验证码是 **9004** 不是 9104， 吐血。。。

**注： 只有在无头模式下截图才是正常的，有头模式可能需要设置截图大小**

* task7 

模拟登陆

两种登录方式：

1. 利用 cookies 维持登录后的session会话 
2. 利用 JWT(Json With Token)，在请求头部添加 jwt 信息，维持登录状态 

cookies 测试网站：https://login2.scrape.cuiqingcai.com/
JWT 测试网站：https://login3.scrape.cuiqingcai.com/

* js-obfuscate

利用 node.js 的 `javascript-obfuscator` 库，尝试了一下 JavaScript 混淆技术

包括代码压缩、变量名混淆、僵尸代码注入、代码自我保护、调试保护、域名锁定等等

简单了解了一下加密技术，Emscripten 和 WebAssembly 等

Emscripten 和 WebAssembly 等 能将 C/C++ 转成 JavaScript 引擎可以运行的代码。可以将一些核心的功能利用 C/C++ 语言实现，形成浏览器字节码的形式。然后在 JavaScript 中调用
