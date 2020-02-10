class Version:
    def __init__(self, version):
        self.pre_proces(version)
        self.version = version.split('.')

    def pre_proces(self, version):
        version = version.replace('-', '')
        version = version.replace('prealpha', 'p')
        version = version.replace('alpha', 'a')
        version = version.replace('beta', 'b')
        return version

    def __eq__(self, other):
        if len(self.version) == len(other.version):
            for i in range(len(self.version)):
                if not (self.version[i] == other.version[i]):
                    return False
            return True
        return False

    # TODO
    def __gt__(self, other):
        print('--------')
        print(self.version)
        print(other.version)

        # get min from 2 versions
        compare_len = len(self.version) if len(self.version) < len(other.version) else len(other.version)
        


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0'),
    ]

    for version_1, version_2 in to_test:
        #assert Version(version_1) < Version(version_2), 'le failed'
        #assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()