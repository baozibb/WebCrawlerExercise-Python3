from pyquery import PyQuery as pq
import requests

'''
三种方式初始化 pyquery 对象
1. 直接传入字符串
2. 传入 url
3. 传入文件

'''


html = '''
<div id="container">
    <ul class="list">
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="blod">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth iten</a></li>
    </ul>
</div>
'''

# 字符串初始化
doc = pq(html)
# print(type(doc))
# print(doc('li'))
# print(type(doc('li')))


# doc = pq(url="https://cuiqingcai.com/")  # url 初始化
# doc = pq(requests.get("https://cuiqingcai.com/").text)
# # doc = pq(filename="./demo.html", encoding='utf-8') # 文件初始化（有点问题）
# print(doc("TiTle"))


# 初步尝试 items()

# li_list = doc("#container .list li")
# print(li_list)
# for item in li_list.items():
#     print(item.text())


# 子节点

# items = doc('.list')
# print(type(items))
# print(items)
# # li_list = items.find('li')  # 这里的 find 查找所有的子孙节点
# li_list = items.children('.active') # children 仅查找子节点
# print(type(li_list))
# print(li_list)


# 父节点

# items = doc(".blod")
# print(items)
# # parent = items.parent()  # 返回直接父节点
# parents = items.parents()  # 返回祖先节点（所有父节点）
# parents = items.parents(".list")  # 查找特定的祖先节点
# print(type(parents))
# print(parents)


# 兄弟节点

# items = doc(".list .item-0.active")
# print(items)
# # print(items.siblings())  # 选取所有节点的所有兄弟节点
# print(items.siblings(".item-0"))  # 选取满足一定条件的兄弟节点


# 遍历

# items = doc(".list .item-0")
# i = 0
# for i, item in items.items():
#     print(f"{i}:\t {str(item)}")
#     i = i + 1


# 获取信息

# 获取属性 attr
# li_a = doc(".active.item-0 a")
# print(li_a)
# print(li_a.attr('href'))
# # 或是
# print(li_a.attr.href)

# print(doc("a").attr.href)  # 多个节点，只会调用第一个节点的属性
# for item in doc("a").items():
#     print("-", item.attr.href)

# # 获取文本 text
# item = doc(".active.item-0 a")
# print(item.text())  # 如果包含多个节点，返回的是所有节点内部的内容
# # 获取标签内完整内容 html
# print(item.html())  # 这里需要注意，如果有多个节点，返回的是第一个节点的 html 信息


# 节点操作
item = doc(".active.item-0")
print(item)

# # 增加/删除 class 属性信息
# item.removeClass("active")
# print(item)
# item.add_class("active-add")
# print(item)

# 操作其他信息
item.attr("name", "rock")
print(item)
item.text("hello baby")
print(item)
item.html("hello world")
print(item)

# remove


# 伪选择器
