学习的时候，到代理池这时，由于一些基础东西没整明白，耽误了好一阵，好在整个项目代码量不大。断断续续的，终于在今天对着 github 敲完了一遍，哈哈哈哈哈哈哈

具体参考崔老师的博客：[[Python3网络爬虫开发实战] 9.2-代理池的维护](https://cuiqingcai.com/7048.html) 和项目地址：[ProxyPool](https://github.com/Python3WebSpider/ProxyPool)

# 代理池介绍

爬虫的反爬方法有很多，最简单的就是更改 headers。不过有当用同一 IP 爬取一个网站过于频繁的时候，这个 IP 很容易会被网站封掉。所以通常，为了爬取网站时自己的 IP 被封，都会使用代理。而且为了爬虫运行正常，一般会经常更换代理。使用代理的优势不止防止被封这一点，有时候也可以达到突破访问限制，访问一些正常访问不了的网站。

那么如何获取 IP 呢？其实网上有很多免费的代理网站，不过里面的 IP 地址大多是不好使的，不过付费的很多时候又没有必要。这时候就需要代理池了。代理池的作用是爬取很多 IP 代理，保存起来，然后验证代理是否可用，当需要使用的时候，就可以从其中取出可用的代理。是不是感觉很酷？

从功能上看，代理池的基本架构就分为四部分：

* 获取模块（Getter）：从各个免费的代理网站上爬取 IP 代理。

* 存储模块（Store）： 将爬取的 IP 代理存起来，当需要使用时，从中取出有效的代理。这里如何存取更新是关键，使用 redis 中的有序集合（Sorted Set）进行存储。给每个代理设置一个分数，当刚存入数据库时，初始分数设为 10。测试更新时，如果检测到代理可用，则设成最大值 100；否则，如果检测到不可用，则每次减一，直到减到最小，删除该代理。

* 测试模块（Tester）： 测试是通过使用代理访问一个特定网站，看访问是否成功。每次测试，都会更新一下代理的分数。

* 接口模块（Server）： 由于是存放的数据库中的，如果每次取用都要暴露数据库信息，不太方便，也不安全。因此，这里使用 flask 做了一个简单的后台服务端。

下面是代理池的框架流程（盗图）：

![IP 代理池架构](https://img-blog.csdnimg.cn/20200509164005502.png)

这就是代理池的基本思路，代码也不多，项目的可扩展性比较好，下面具体介绍一下每个模块。

# 代理池代码解释

### 获取模块

获取模块是爬取各大免费 IP 代理网站，获取到 IP。免费网站主要有： [西刺免费代理](http://www.xicidaili.com)、 [快代理](https://www.kuaidaili.com/free/)、[66免费代理](http://www.66ip.cn/index.html)等等。有一点比较好的是，这些网站结构比较简单，代理比较好爬，如果不考虑反爬措施的话，还是很亲民的。

代理池中，所有的获取代理代码都继承自 BaseCrawler，这里增加了一些爬取时的头部信息。

所有爬取网站的代码，都可以通过继承它来放到项目中，扩展性很好，我尝试写了个西刺代理网站的代码：

```python
# -*- coding:utf-8  -*-
from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
from pyquery import PyQuery as pq
BASE_URL = 'https://www.xicidaili.com/nn/{page}'
MAX_PAGE = 200
class XicidailiCrawler(BaseCrawler):
    '''
    xicidaili crawler, https://www.xicidaili.com/nn/
    '''
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        '''parse html file to get proxies
        :param html: the text of website
        :type html: str

        :return: the generator of proxies
        :rtype: Proxy
        '''
        doc = pq(html)
        for tr in doc('#ip_list tr:gt(0)').items():
            host = tr.find('td:nth-child(2)').text()
            port = tr.find('td:nth-child(3)').text()
            if host and port:
                proxy = Proxy(host=host, port=port)
                yield proxy
if __name__ == '__main__':
    crawler = XicidailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
```

代码可以运行，不过西刺代理有一些反爬机制，不能太过频繁（我就是太快了，导致它把我的 IP 给封掉了），所以并没有放到最后的项目中。

### 存储模块

存储时，使用的是 Redis 数据库。由于之前没使用过，现学了一下，感觉这个库有点酷啊。跟 MongoDB 一样，是 key-value 类型的数据库，不过 Redis 支持五种数据类型，这里用的是 Sorted Set 有序集合类型。

需要注意的是，使用前要安装好 Redis。


这里主要是记录了一下数据库的增删改查。增加代理时设置初始分数；更改代理时，设置分数减一或是变为最大值；删除时


### 测试模块

测试时，需要使用一个测试网站，用代理去访问它。通常是要爬取哪个网站就用哪个网站进行测试，不过通用的话，使用的是百度，毕竟比较稳定。

测试时，根据代理是否可用，设置数据库中的代理分数。如果可用，直接设成最大值；不可用，分数减一。当分数减到比最小值还小时，删除该代理。


### 接口模块

接口模块不是必须的，其实前三个模块组合起来就已经实现了代理池的所有功能了。接口模块只是让项目更完善，将底层封装起来，项目更完整。

这里做接口使用的是 flask，我同样也没接触过，不过好在上手很容易，项目中也没用到多难的东西，很容易理解。直接看代码就好。

接口模块的测试结果如下：
![代理池接口模块的测试结果](https://img-blog.csdnimg.cn/20200509164930988.png)




# 运行

这里只设置了使用常规方式运行，并没有使用 Docker 等。

需要先行配置环境，最好使用 python 虚拟环境。

`pip install -r requirements.txt`

`python run.py`

访问 http://localhost:5555/random 即可获取一个随机可用代理。


# 最后


虽然用的时间比较长，但不得不说，这个项目还是比较好的。代码量虽然不多，但确实让我学到了很多东西，对 python 语言也有了一个更深的认识。最重要的是，对新手很友好。不多bb，强烈推荐崔大的教程。


