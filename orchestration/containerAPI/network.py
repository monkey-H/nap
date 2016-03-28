from docker import Client

class Network(object):
    """
    Represents a docker network
    """

    def __init__(self, name, driver):
        self.name = name
        self.driver = driver

    @staticmethod
    def create_network(client, name, driver):
        client.create_network(name=name, driver=driver)

    @staticmethod
    def get_networks(client):
        ans = []
        networks = client.networks()
        for network in networks:
            item = {}
            item["name"] = network["Name"]
            item["id"] = network["Id"]
            item["driver"] = network["Driver"]
            ans.append(item)

        return ans

    @staticmethod
    def remove_network(client, name):
        client.remove_network(net_id=name)
