import requests
from cone.spider import BaseDownloader
from pyquery_ex import PyQuery
import chardet
from news.parser.common import CommonParser


url = 'http://v.people.cn/n1/2019/0611/c222296-31130062.html'
res = requests.get(url,timeout=30, headers=BaseDownloader.headers)

res.encoding = chardet.detect(res.content)['encoding']
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(res.text)
doc = PyQuery(res.text)

max_dom = None
max_len = 0
doc.remove('script')
doc.remove('a')
contains = doc('body')
# for contain in contains.items():
#     if len(contain.text()) > max_len:
#         max_len = len(contain.text())
#         max_dom = contain

def get_dom_by_density(dom:PyQuery, min_density=0.7, depth=5):
    children = dom.children()
    max_len_dom = dom("#abcdefg")
    max_len = 0
    text_num = 0
    child_lens = len(children)
    for child in children.items():
        lens = len(child.text())
        if lens and lens > 10:
            text_num += 1
            if max_len < lens:
                max_len = lens
                max_len_dom = child
    density = text_num / (child_lens or 1e9)
    if density < min_density and depth > 0:
        density, dom, max_len, _ = get_dom_by_density(max_len_dom, min_density, depth=depth-1)
    # print(dom.text(), density, lens, depth)
    return density, max_len_dom, max_len, depth

# density, dom, lens_, depth = get_dom_by_density(contains)

def get_dom_density(dom:PyQuery, min_density=0.7, depth=5):
    children = dom.children()
    max_len_dom = dom("#abcdefg")
    max_len = 0
    text_num = 0
    child_lens = len(children)
    print("-----")
    for child in children.items():
        lens = len(child.text())
        print(lens)
        
        if lens or str(child).startswith('<p'):
            text_num += 1
            if max_len < lens:
                max_len = lens
                max_len_dom = child
    density = text_num / (child_lens or 1e9)
    return density, max_len_dom, max_len, dom

# density, dom, lens, origin_dom = get_dom_density(contains)
# if density < 0.5:
#     density, dom, lens, origin_dom = get_dom_density(dom)
#     if density < 0.5:
#         density, dom, lens, origin_dom = get_dom_density(dom)
#         # print(dom.text(), density, lens)
#         if density < 0.5:
#             density, dom, lens, origin_dom = get_dom_density(dom)
#             for index, i in enumerate(origin_dom.children().items()):
#                 print(f"{index}->{str(i)}")
#                 print(i.html().startswith('<p') if i.html() else "----")
#             print(density)
#             if density < 0.5:
#                 density, dom, lens, origin_dom = get_dom_density(dom)
                # if density < 0.5:
                #     density, dom, lens = get_dom_density(dom)
                #     if density < 0.5:
                #         density, dom, lens = get_dom_density(dom)

# print(dom.text(), density, lens_, depth)
# print("max-dom", max_dom.text())
# print("max-len,", max_len)
# max_dom = max_dom.children().eq(1)
# print(max_dom.text())
# max_dom = max_dom.children().eq(0)
# print(max_dom.text())
# for sub in max_dom.children().items():
#     print(len(sub.text()))
# print(max([len(dom.text()) for dom in contains.items()]))
res.meta = {'item': {'title': '科？'}, 'list_time': '2019-10-2'}
result = CommonParser({'url': 'http://www.people.com.cn/n1/2019/0613/c32306-31134977.html',
'id': '1'}, None).parse_detail(res)
for i in result:
    print(i)
# raise KeyboardInterrupt
# print(doc('title').text())
# print(doc('div:contains("乐平公路分局组织道班开展养护作业安全培训（图）")').text())
# contains = doc('div:contains("景德镇媒体答谢宴暨碧桂园昌南府见面会盛情举行")')
# if contains:
#     for index, item in enumerate(contains.items()):
#         print(f'index->{index}', item.text())
#     print(contains.eq(2))
#     for i in range(len(contains)):
#         print(f"{i}, {len(contains)}", contains.eq(len(contains)-1).text())
    # title_dom = contains.eq(len(contains))
    # print(title_dom.text())
