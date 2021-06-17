from datetime import datetime

import torch
from django.http import JsonResponse
from django.views.generic import TemplateView
from matplotlib import pyplot as plt
from scipy.special import expit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from Project.settings import MEDIA_ROOT
from Project.wsgi import det_transformer, det_face_extractor, det_device, det_net
from profiles.models import Profile
from reports.models import Report
from uploads import utils
from uploads.models import Uploads

@login_required()
def upload_view(request):
    if request.method == 'POST':
        video_file = request.FILES.get('file')
        if len(Uploads.objects.filter(file_name=video_file)) == 0:
            upload = Uploads.objects.create(author=Profile.objects.get(user=request.user),
                                            upload_id=utils.generate_code(),
                                            created=datetime.now(), file_name=video_file,
                                            changed_file_name=video_file)
            upload_dict = {your_key: upload.__dict__[your_key] for your_key in
                           ['upload_id', 'file_name', 'changed_file_name', 'created']}
            upload_dict['ex'] = False
            print(upload_dict)
            return JsonResponse(upload_dict)
        else:
            upload = Uploads.objects.filter(file_name=video_file).first()
            report = Report.objects.filter(upload=upload)
            if len(report) < 1:
                upload_dict = {your_key: upload.__dict__[your_key] for your_key in
                               ['upload_id', 'file_name', 'changed_file_name', 'created']}
                upload_dict['ex'] = True
                upload_dict['already'] = False
                print(upload_dict)
                return JsonResponse(upload_dict)
            else:
                return report.first()

@login_required()
def detect_view(request):
    if request.method == 'POST':
        result = None
        post_data = request.POST

        print(str(MEDIA_ROOT) + post_data['changed_file_name'])
        video_faces = det_face_extractor.process_video(MEDIA_ROOT / post_data['changed_file_name'])

        im_face = video_faces[0]['faces'][0]

        plt.figure(0, figsize=(10, 10))
        plt.imshow(im_face)
        face_sample = utils.get_graph()
        plt.close()

        faces_t = torch.stack(
            [det_transformer(image=frame['faces'][0])['image'] for frame in video_faces if len(frame['faces'])])

        with torch.no_grad():
            faces_real_pred = det_net(faces_t.to(det_device)).cpu().numpy().flatten()

        plt.figure(1, figsize=(20, 10))
        plt.stem([f['frame_idx'] for f in video_faces if len(f['faces'])], expit(faces_real_pred),
                 use_line_collection=True)
        frame_pred_graph = utils.get_graph()
        plt.close()

        no_of_frames = len(faces_real_pred)

        pred_mean = expit(faces_real_pred.mean()) * 100

        if pred_mean > 75:
            result = 'FAKE'
        else:
            result = 'REAL'

        print('Average score of video: {:.4f}'.format(pred_mean))

        upload = Uploads.objects.get(upload_id=post_data['upload_id'])
        author = Profile.objects.get(user=request.user)
        name = f'Report generated on Date {upload.get_upload_date()} for file: {upload.get_upload_filename()}'
        Report.objects.create(name=name,
                              upload=upload, face_sample=face_sample,
                              author=author, result=result,
                              # frame_graph=frame_graph,
                              no_of_frames=no_of_frames, pred_mean=pred_mean, frame_pred_graph=frame_pred_graph
                              )

    return JsonResponse({'ex': False})


class UploadTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'uploads/upload.html'
