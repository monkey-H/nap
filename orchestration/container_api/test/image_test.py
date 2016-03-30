from api.image import Image
from docker import Client

list = Image.get_list('114.212.87.52:2376', '1.21')

# for item in list:
    # print item

client = Client(base_url='114.212.87.52:2376', version='1.21')
im = Image(client=client, name='busybox')

print im.name
print im.size
print im.create_time
print im.tag

Image.destroy_image(url='114.212.87.52:2376', version='1.21', name='test')
