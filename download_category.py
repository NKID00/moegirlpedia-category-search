from json import dump, JSONDecodeError
from operator import itemgetter
from typing import List, Optional, Tuple

from httpx import Client

from util import __version__, root_dir, user_agent


def download_one_page(
    client: Client, title: str, cmcontinue: Optional[str]
) -> Tuple[Optional[str], List[Tuple[int, str]]]:
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'format': 'json',
        'cmprop': 'title',
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


def download_all(client: Client, title: str) -> List[Tuple[int, str]]:
    i = 1
    print('正在下载第 1 页...', end=' ')
    cmcontinue, data = download_one_page(client, title, None)
    result = data
    print(f'已获取 {len(data)} 个，共获取 {len(result)} 个', end='\r')
    while cmcontinue is not None:
        i += 1
        print(f'正在下载第 {i} 页...', end=' ')
        cmcontinue, data = download_one_page(client, title, cmcontinue)
        result.extend(data)
        print(f'已获取 {len(data)} 个，共获取 {len(result)} 个', end='\r')
    if len(result) == 0:
        print()
        raise KeyError(f'Category:{title} 为空！')
    print()
    return result

def write_one(data, title):
    root_dir.mkdir(exist_ok=True)
    with open(root_dir / f'{title}.json', 'w', encoding='utf8') as f:
        dump(data, f, ensure_ascii=False, separators=(',', ':'))

def download_and_write(title: str):
    with Client(headers={
        'User-Agent': user_agent
    }) as client:
        write_one(download_all(client, title), title)
        


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
