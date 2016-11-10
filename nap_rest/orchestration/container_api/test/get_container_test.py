from api.container import Container

url = '114.212.87.52:2376'
version = '1.21'

def get_container(url, version, name):
    con =  Container.get_container(url, version, name)
    print con.ip
    print con.cmd
    print con.network.name

if __name__ == "__main__":
    get_container(url, version, "test")
