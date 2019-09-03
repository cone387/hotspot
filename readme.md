# 文档说明

## api

### 查询有哪些来源热点
* /api/config/website/enable
```python
# 返回
{
    "success": True, 
    "code": 0,
    "data": [
        {"name": "微博热搜", 
        "url": "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6", 
        "category": "综合"}
    ]
}
```

* /api/config/website/crawl_time?id=1
```python
# 返回网站热点的最后更新时间, id为来源id。比如新浪热搜为1
{
    "success": True, 
    "data": {"id": 1, 
        "name": "微博热搜", 
        "last_runtime": "2019-08-26 21:14:00"
        }, 
    "code": 0}
```

* api/data/website?id=1
```python
# 获取网站最新数据
{"success": True, 
"data": [
    {"title": "中国18个自由贸易区", "url": "https://s.weibo.com/weibo?q=%23%E4%B8%AD%E5%9B%BD18%E4%B8%AA%E8%87%AA%E7%94%B1%E8%B4%B8%E6%98%93%E5%8C%BA%23&Refer=top"}, 
    {"title": "费德勒状态", "url": "https://s.weibo.com/weibo?q=%E8%B4%B9%E5%BE%B7%E5%8B%92%E7%8A%B6%E6%80%81&Refer=top"}, 
    {"title": "苹果将捐款修复亚马逊雨林", "url": "https://s.weibo.com/weibo?q=%23%E8%8B%B9%E6%9E%9C%E5%B0%86%E6%8D%90%E6%AC%BE%E4%BF%AE%E5%A4%8D%E4%BA%9A%E9%A9%AC%E9%80%8A%E9%9B%A8%E6%9E%97%23&Refer=top"}, 
    {"title": "初秋少女范穿搭", "url": "https://s.weibo.com/weibo?q=%23%E5%88%9D%E7%A7%8B%E5%B0%91%E5%A5%B3%E8%8C%83%E7%A9%BF%E6%90%AD%23&Refer=top"}, 
    {"title": "股市", "url": "https://s.weibo.com/weibo?q=%E8%82%A1%E5%B8%82&Refer=top"}
    ],
   "code": 0}
```