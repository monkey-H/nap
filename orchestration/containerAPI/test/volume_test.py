from api.volume import Volume

url = '114.212.87.52:2376'
version='1.21'

def test():
    # print Volume.remove(url, version, 'fufu')
    Volume.create(url, version, 'fufu')
    Volume.inspect(url, version, 'fufu')
    Volume.lists(url, version)

if __name__ == '__main__':
    test()
