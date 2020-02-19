#!/usr/bin/python3.6

# in python 3.6 I don't need to use functools.total_ordering

import typing

class Version:
    def __init__(self, version : str):
        self.version = self.pre_proces(version)

    def pre_proces(self, version : str) -> typing.Iterable[typing.Iterable[int]]:
        version = version.replace('-', '')
        # replase full names
        version = version.replace('prealpha', '|-4|')
        version = version.replace('alpha', '|-3|')
        version = version.replace('beta', '|-2|')
        version = version.replace('rc', '|-1|')
        # replase short
        version = version.replace('b', '|-2|')
        version = version.replace('a', '|-3|')
        version = version.split('.')

        # [1, 2, 3|-3|_, 4] of [1, 2, 3|-3|4, 5]
        for block_i, block_v in enumerate(version):
            version[block_i] = block_v.split('|')

        # [[1], [2], [3,-3,_] , [4]]
        for block_i, block_v in enumerate(version):
            for number_i, number_v in enumerate(version[block_i]):
                version[block_i][number_i] = 0 if number_v == '' else int(number_v)

        # [[1], [0], [0, -1, 0]]
        if len(version) == 3:
            version.append([0])
          
        # [[1], [0], [0, -1, 0], [0]]
        return version

    def __eq__(self, other : typing.TypeVar('Version')) -> bool:
        
        for block_i, _ in enumerate(self.version):
            for number_i, _ in enumerate(self.version[block_i]):
                if not( self.version[block_i][number_i] == other.version[block_i][number_i]):
                    return False
        
        return True

    
    # TODO
    def __gt__(self, other : typing.TypeVar('Version')) -> bool:

        min_len_version = min([len(self.version),len(other.version)])

        for block_i, _ in enumerate(self.version):
            for number_i, _ in enumerate(self.version[block_i]):
                if not( self.version[block_i][number_i] == other.version[block_i][number_i]):
                    return False
        

    def old__gt__(self, other : typing.TypeVar('Version')) -> bool:

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
        ('1.0.0-rc.1', '1.0.0')
        #,('1.0.0','1.0.00')
    ]

    for version_1, version_2 in to_test:
        #assert Version(version_1) < Version(version_2), 'le failed'
        #assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()