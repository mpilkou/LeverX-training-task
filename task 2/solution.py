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
            zeros_if_none = [0]*3
            for number_i, number_v in enumerate(version[block_i]):
                zeros_if_none[number_i] = 0 if number_v == '' else int(number_v)
            version[block_i] = zeros_if_none

        # [[1,0,0], [0,0,0], [0, -1, 0]]
        zeros_if_size_less_4 = [[0]*3]*4
        for block_i, block_v in enumerate(version):
            zeros_if_size_less_4 [block_i] = block_v
        
        version = zeros_if_size_less_4
          
        # [[1], [0], [0, -1, 0], [0]]
        return version

    def __eq__(self, other : typing.TypeVar('Version')) -> bool:
        
        for block_i, _ in enumerate(self.version):
            for number_i, _ in enumerate(self.version[block_i]):
                if not( self.version[block_i][number_i] == other.version[block_i][number_i]):
                    return False
        
        return True

    
    def __gt__(self, other : typing.TypeVar('Version')) -> bool:
        for block_i, _ in enumerate(self.version):
            for number_i, _ in enumerate(self.version[block_i]):
                if self.version[block_i][number_i] < other.version[block_i][number_i]:
                    return False
                elif self.version[block_i][number_i] > other.version[block_i][number_i]:
                    return True

        return True 


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0'),
        ('1.0.0','1.0.0.1')
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()