#!/usr/bin/python3.6

# in python 3.6 I don't need to use functools.total_ordering

import typing

class Version:
    def __init__(self, version : str):
        version = self.pre_proces(version)
        self.version = version.split('.')

    def pre_proces(self, version : str) -> str:
        version = version.replace('-', '')
        version = version.replace('prealpha', 'P')
        version = version.replace('alpha', 'a')
        version = version.replace('beta', 'b')
        return version

    def __eq__(self, other : typing.TypeVar('Version')) -> bool:
        if len(self.version) == len(other.version):
            for i,_ in enumerate(self.version):
                if not (self.version[i] == other.version[i]):
                    return False
            return True
        return False
    
    def __gt__(self, other : typing.TypeVar('Version')) -> bool:

        # get min from 2 versions
        compare_len = len(self.version) if len(self.version) < len(other.version) else len(other.version)

        for i in range(compare_len):
            # get min from vetsions beetween .-.
            compare_len_i = min([len(self.version[i]),len(other.version[i])])
            for j in range(compare_len_i):
                if self.version[i][j].isnumeric() and other.version[i][j].isnumeric():
                    # [0-9] > [0-9]
                    if self.version[i][j] > other.version[i][j]:
                        return True
                    elif self.version[i][j] < other.version[i][j]:
                        return False
                    # else: 1 == 1
                # [0-9] > [a-]
                elif self.version[i][j].isnumeric():
                    return True

                # [a-] > [0-9]
                elif other.version[i][j].isnumeric():
                    return False

                # [a-] > [a-]
                else:
                    # P < a < b < r : ascii
                    if self.version[i][j] > other.version[i][j]:
                        return True
                    elif self.version[i][j] < other.version[i][j]:
                        return False
                    # else: a == a
            # 0rc < 0
            if len(self.version[i]) < len(other.version[i]):
                return True

        # 1.0.0.1 > 1.0.0
        if len(self.version) > len(other.version):
            return True
        # self == other
        return False   


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0'),
        ('1.0.0','1.0.00')
    ]

    for version_1, version_2 in to_test:
        #assert Version(version_1) < Version(version_2), 'le failed'
        #assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()