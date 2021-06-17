import base64
import os
import uuid
from io import BytesIO

from matplotlib import pyplot as plt


def path_and_rename(instance, filename):
    print(filename)
    upload_to = 'uploads'
    ext = filename.split('.')[-1]
    instance.file_name = filename
    filename = '{}.{}'.format(instance.author.user.username + '_' + instance.created.strftime('%Y-%m-%d_%H-%M-%S'), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
