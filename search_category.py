from json import load, JSONDecodeError
from cmd import Cmd
from itertools import zip_longest
from webbrowser import open as webbrowser_open
from urllib.parse import quote
from typing import Set

from util import __version__, ROOT_DIR
from download_category import download_and_write, write_one

def read_one(title: str, include_subcat: bool) -> Set[str]:
    path = ROOT_DIR / f'{title}.json'
    if path.exists():
        print(f'正在读取分类"{title}"...')
        with open(path, 'r', encoding='utf8') as f:
            subcats, data = load(f)
        data = set(data)
        if include_subcat:
            for subcat in subcats:
                data |= read_one(subcat, True)
        return data
    else:
        print(f'正在下载分类"{title}"...')
        if download_and_write(title):
            return read_one(title, include_subcat)
        else:
            return set()

class SearchCli(Cmd):
    intro = (
        '|<分类标题> -> 取并集\n'
        '&<分类标题> -> 取交集\n'
        '-<分类标题> -> 取差集\n'
        '^<分类标题> -> 取对称差集\n'
        '在以上命令前加 * 则包括子分类（警告：一些分类可能拥有极其庞大的子分类网络）\n'
        's<分类标题> -> 保存当前集合\n'
        'p -> 显示当前集合\n'
        'o[每次打开的数量，0 为全部，默认 10]'
        ' -> 显示当前集合并分批在浏览器中打开对应页面\n'
        'exit -> 退出'
    )
    prompt = '>>> '

    def preloop(self):
        self.data = set()

    def default(self, line: str) -> bool:
        if line == 'exit':
            return True

        try:
            length = len(self.data)
            if line.startswith(('*', '|', '&', '-', '^')):
                if line.startswith('*'):
                    include_subcat = True
                    line = line[1:]
                else:
                    include_subcat = False
                if line.startswith('|'):
                    self.data |= read_one(line[1:], include_subcat)
                elif line.startswith('&'):
                    self.data &= read_one(line[1:], include_subcat)
                elif line.startswith('-'):
                    self.data -= read_one(line[1:], include_subcat)
                elif line.startswith('^'):
                    self.data ^= read_one(line[1:], include_subcat)
                else:
                    print('未知的命令')
                    return False
            elif line.lower().startswith('s'):
                write_one([], sorted(self.data), line[1:])
                return False
            elif line.lower().startswith('p'):
                for title in sorted(self.data):
                    print(title)
                print(f'共 {len(self.data)} 个')
                return False
            elif line.lower().startswith('o'):
                if line[1:] == '':
                    chunk_size = 10
                else:
                    try:
                        chunk_size = int(line[1:])
                    except ValueError:
                        print('数值不正确！')
                        return False
                    if chunk_size < 0:
                        print('数值不正确！')
                        return False
                if chunk_size == 0:
                    for page in sorted(self.data):
                        print(page)
                        webbrowser_open(
                            f'https://zh.moegirl.org.cn/'
                            f'{quote(page, encoding="utf-8")}',
                            new=2
                        )
                    print(f'已打开 {len(self.data)} 个页面')
                else:
                    count = 0
                    sorted_data = iter(sorted(self.data))
                    for chunk in zip_longest(*[sorted_data]*chunk_size):
                        for page in chunk:
                            if page is not None:
                                print(page)
                                webbrowser_open(
                                    f'https://zh.moegirl.org.cn/'
                                    f'{quote(page, encoding="utf-8")}',
                                    new=2
                                )
                                count += 1
                        if len(self.data) - count > 0:
                            input(
                                f'已打开 {count} 个页面，'
                                f'还剩 {len(self.data) - count} 个，'
                                f'按回车继续...'
                            )
                    print(f'已打开 {count} 个页面')

                return False
            else:
                print('未知的命令')
                return False
        except JSONDecodeError as e:
            print(
                'JSON 解析失败，'
                '可能需要使用浏览器访问萌娘百科并手动进行人机验证'
            )
        else:
            print(f'{length} -> {len(self.data)}')
        return False


def main():
    print(f'moegirlpedia-category-search v{__version__}\n')
    SearchCli().cmdloop()


if __name__ == '__main__':
    main()

