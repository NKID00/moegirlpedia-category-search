from json import dump, JSONDecodeError
from operator import itemgetter
from typing import List, Optional, Tuple

from httpx import Client, HTTPStatusError

from util import __version__, ROOT_DIR, USER_AGENT, PROXY

def download_one_page(
    client: Client, title: str, cmtype: str, cmcontinue: Optional[str]
) -> Tuple[Optional[str], List[str]]:
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'format': 'json',
        'cmprop': 'title',
        'cmtype': cmtype,
        'cmlimit': '5000',
        'cmtitle': f'Category:{title}'
    }
    if cmcontinue is not None:
        params['cmcontinue'] = cmcontinue
    r = client.get('https://zh.moegirl.org.cn/api.php', params=params)
    r.raise_for_status()
    data = r.json()
    try:
        cmcontinue = data['continue']['cmcontinue']
    except KeyError:
        cmcontinue = None
    return cmcontinue, list(map(
        itemgetter('title'),
        data['query']['categorymembers']
    ))


def download_all(client: Client, title: str) -> Tuple[List[str], List[str]]:
    i = 1
    print('正在下载子分类信息的第 1 页...', end=' ')
    cmcontinue, data = download_one_page(client, title, 'subcat', None)
    data = list(map(
        lambda s: s.replace('Category:', '').replace('分类:', ''),
        data
    ))
    subcat = data
    print(f'已获取 {len(data)} 个，共获取 {len(subcat)} 个子分类', end='\r')
    while cmcontinue is not None:
        i += 1
        print(f'正在下载子分类信息的第 {i} 页...', end=' ')
        cmcontinue, data = download_one_page(
            client, title, 'subcat', cmcontinue
        )
        data = list(map(
            lambda s: s.replace('Category:', '').replace('分类:', ''),
            data
        ))
        subcat.extend(data)
        print(f'已获取 {len(data)} 个，共获取 {len(subcat)} 个子分类', end='\r')
    print()

    i = 1
    print('正在下载页面信息的第 1 页...', end=' ')
    cmcontinue, data = download_one_page(client, title, 'page', None)
    result = data
    print(f'已获取 {len(data)} 个，共获取 {len(result)} 个页面', end='\r')
    while cmcontinue is not None:
        i += 1
        print(f'正在下载页面信息的第 {i} 页...', end=' ')
        cmcontinue, data = download_one_page(
            client, title, 'page', cmcontinue
        )
        result.extend(data)
        print(f'已获取 {len(data)} 个，共获取 {len(result)} 个页面', end='\r')
    print()

    if len(subcat) == 0 and len(result) == 0:
        print(f'分类"{title}"为空！')

    return subcat, result

def write_one(subcat: List[str], data: List[str], title: str):
    ROOT_DIR.mkdir(exist_ok=True)
    with open(ROOT_DIR / f'{title}.json', 'w', encoding='utf8') as f:
        dump([subcat, data], f, ensure_ascii=False, separators=(',', ':'))

def download_and_write(title: str) -> bool:
    with Client(headers={'User-Agent': USER_AGENT}, proxies=PROXY) as client:
        try:
            write_one(*download_all(client, title), title)
        except HTTPStatusError as e:
            print()
            print(f'HTTP 状态异常：{e.response.status_code}')
            return False
        else:
            return True
        


def main():
    print(f'moegirlpedia-category-search v{__version__}\n')
    try:
        download_and_write(input('标题（不包括前缀）：'))
    except JSONDecodeError:
        print(
            'JSON 解析失败，'
            '可能需要使用浏览器访问萌娘百科并手动进行人机验证'
        )
    else:
        print('完成')


if __name__ == '__main__':
    main()
