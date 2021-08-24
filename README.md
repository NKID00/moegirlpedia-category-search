# 萌娘百科分类搜索工具

> 黑发蓝瞳双马尾有呆毛又是黑客的人物一共有哪些？

## 用法

需要 `python>=3.6`。

安装依赖：

```sh
$ python3 -m pip install -r requirements.txt
```

启动交互式命令行界面：

```sh
$ python3 search_category.py
```

### 示例：查找黑发蓝瞳双马尾有呆毛又是黑客的人物

注：该示例运行于 2021.8.24，数据可能会有所出入

```
$ python3 search_category.py
moegirlpedia-category-search v0.1.1

... 略过一些提示 ...

>>> |人物       <- 将当前集合（空集）与人物分类中的条目进行并集操作
正在下载第 60 页... 已获取 473 个，共获取 29973 个      <- 这是从萌娘百科下载的分类数据的情况
0 -> 29973      <- 这是目前集合里条目数量的变动情况
>>> &黑发       <- 将当前集合（人物分类）与黑发分类中的条目进行交集操作，即只取黑发的人物
正在下载第 11 页... 已获取 239 个，共获取 5239 个
29973 -> 4824   <- 还剩下这么多条目
>>> &蓝瞳       <- 继续取交集
正在下载第 11 页... 已获取 355 个，共获取 5355 个
4824 -> 582
>>> &双马尾
正在下载第 2 页... 已获取 202 个，共获取 702 个
582 -> 6
>>> &呆毛
正在下载第 3 页... 已获取 146 个，共获取 1146 个
6 -> 4
>>> &黑客
正在下载第 1 页... 已获取 42 个，共获取 42 个
4 -> 1          <- 只剩一个条目啦
>>> p           <- 显示出当前集合中的条目标题
赛小盐
共 1 个
>>> o           <- 在浏览器中打开当前集合中的条目对应页面
已打开 1 个页面
```

除了示例里的操作，还支持取差集和取对称差集操作（也就是说甚至可以寻找有猫耳但没有呆毛的角色），支持保存当前筛选过的集合，具体操作方法请参见程序运行时的提示。

下载的分类和保存的集合都在 `cache/` 目录下。

如果遇到了 `JSON 解析失败，可能需要使用浏览器访问萌娘百科并手动进行人机验证` 提示信息，别慌，照着程序说的用浏览器打开萌百，完成跳出来的验证码就可以继续使用程序了！

注：具体分类的准确性完全依赖于萌娘百科，如果发现分类错误请[{{自己动手}}](https://zh.moegirl.org.cn/Template:%E8%87%AA%E5%B7%B1%E5%8A%A8%E6%89%8B)（雾

## 版权

版权所有 © NKID00 2021

使用 MIT License 进行许可。
