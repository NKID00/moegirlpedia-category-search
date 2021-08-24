from json import load, JSONDecodeError
from cmd import Cmd
from itertools import zip_longest
from webbrowser import open as webbrower_open
from typing import FrozenSet, Tuple

from util import __version__, root_dir
from download_category import download_and_write, write_one

def read_one(title: str) -> FrozenSet[Tuple[int, str]]:
    path = root_dir / f'{title}.json'
    if path.exists():
        with open(path, 'r', encoding='utf8') as f:
            return frozenset(load(f))
    else:
        download_and_write(title)
        return read_one(title)

class SearchCli(Cmd):
    intro = (
        '|<分类标题> -> 取并集\n'
        '&<分类标题> -> 取交集\n'
        '-<分类标题> -> 取差集\n'
        '^<分类标题> -> 取对称差集\n'
        's<分类标题> -> 保存当前集合\n'
        'p -> 显示当前集合\n'
        'o -> 打开当前集合对应页面\n'
        'exit -> 退出'
    )
    prompt = '>>> '

    def preloop(self):
        self.data = frozenset()

    def default(self, line: str) -> bool:
        if line == 'exit':
            return True

        try:
            length = len(self.data)
            if line.startswith('|'):
                self.data = self.data | read_one(line[1:])
            elif line.startswith('&'):
                self.data = self.data & read_one(line[1:])
            elif line.startswith('-'):
                self.data = self.data - read_one(line[1:])
            elif line.startswith('^'):
                self.data = self.data ^ read_one(line[1:])
            elif line.lower().startswith('s'):
                write_one(sorted(self.data), line[1:])
                return False
            elif line.lower().startswith('p'):
                for title in sorted(self.data):
                    print(title)
                print(f'共 {len(self.data)} 个')
                return False
            elif line.lower().startswith('o'):
                it = iter(sorted(self.data))
                count = 0
                for chunk in zip_longest(*[it]*10):
                    for title in chunk:
                        if title is not None:
                            webbrower_open(
                                f'https://zh.moegirl.org.cn/{title}',
                                new=2
                            )
                            count += 1
                    if len(self.data) - count > 0:
                        input(
                            f'已打开 {count} 个页面，'
                            f'还剩 {len(self.data) - count} 个，按回车继续...'
                        )
                    else:
                        print(f'已打开 {count} 个页面')
                return False
            else:
                print('未知的命令')
                return False
        except KeyError as e:
            print(e.args[0])
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

