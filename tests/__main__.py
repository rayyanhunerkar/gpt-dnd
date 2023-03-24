import pytest


def main():
    # extract your arg here
    # logging.log(msg='Extracted arg is ==> %s' % sys.argv[-1], level=1)
    pytest.main(['.', '-s', '--cov-config=.coveragerc', '--cov-report=html'])


if __name__ == '__main__':
    main()
