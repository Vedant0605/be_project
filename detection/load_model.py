import sys

import torch
from torch.utils.model_zoo import load_url

sys.path.append('..')

from .blazeface import FaceExtractor, BlazeFace, VideoReader
from .architectures import fornet, weights
from .isplutils import utils


def export_model():
    net_model = 'Xception'
    train_db = 'DFDC'

    device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
    face_policy = 'scale'
    face_size = 224
    frames_per_video = 60
    print('----------------------------------------------------------')
    print(f'FaceNet Model:{net_model}')
    print(f'Training DataSet:{train_db}')
    print(f'Device:{device}')
    print(f'Face Policy:{face_policy}')
    print(f'Face Size:{face_size}')
    print(f'Frames Per Video:{frames_per_video}')

    model_url = weights.weight_url['{:s}_{:s}'.format(net_model, train_db)]
    net = getattr(fornet, net_model)().eval().to(device)
    net.load_state_dict(load_url(model_url, map_location=device, check_hash=True))

    transformer = utils.get_transformer(face_policy, face_size, net.get_normalizer(), train=False)

    facedet = BlazeFace().to(device)
    facedet.load_weights("detection/blazeface/blazeface.pth")
    facedet.load_anchors("detection/blazeface/anchors.npy")
    videoreader = VideoReader(verbose=False)
    video_read_fn = lambda x: videoreader.read_frames(x, num_frames=frames_per_video)
    face_extractor = FaceExtractor(video_read_fn=video_read_fn, facedet=facedet)
    print('Transformer and Face Extractor Initialized')
    print('----------------------------------------------------------')
    return (transformer, face_extractor, net, device)
