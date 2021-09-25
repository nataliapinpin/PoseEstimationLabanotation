# Works Cited
# https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
#

"""
Structure of keypoints
    0: R ankle
    1: R knee
    2: R hip
    3: L hip
    4: L knee
    5: L ankle
    6: Pelvis
    7: Thorax
    8: Upper neck
    9: Head
    10: R wrist
    11: R elbow
    12: R shoulder
    13: L shoulder
    14: L elbow
    15: L wrist
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import cv2
import numpy as np
import torch
import torch.utils.data
from opts import opts
from model import create_model
from utils.debugger import Debugger
from utils.image import get_affine_transform, transform_preds
from utils.eval import get_preds, get_preds_3d

from demo import is_image
import labanotation_data as lnd
import draw_labanotation as draw

image_ext = ['jpg', 'jpeg', 'png']
mean = np.array([0.485, 0.456, 0.406], np.float32).reshape(1, 1, 3)
std = np.array([0.229, 0.224, 0.225], np.float32).reshape(1, 1, 3)



def parse_video(video_path, images_path):
    cap = cv2.VideoCapture(video_path)
    success = True
    count = 1
    fps = 1
    while success:
        cap.set(cv2.CAP_PROP_POS_MSEC, count*1000)  # 1 fps
        success, image = cap.read()
        if success:
            cv2.imwrite(images_path + f"/{count}.jpg", image)
            count += 1


def get_predictions(image, model, opt):
  s = max(image.shape[0], image.shape[1]) * 1.0
  c = np.array([image.shape[1] / 2., image.shape[0] / 2.], dtype=np.float32)
  trans_input = get_affine_transform(
      c, s, 0, [opt.input_w, opt.input_h])
  inp = cv2.warpAffine(image, trans_input, (opt.input_w, opt.input_h),
                         flags=cv2.INTER_LINEAR)
  inp = (inp / 255. - mean) / std
  inp = inp.transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32)
  inp = torch.from_numpy(inp).to(opt.device)
  out = model(inp)[-1]
  pred = get_preds(out['hm'].detach().cpu().numpy())[0]
  pred = transform_preds(pred, c, s, (opt.output_w, opt.output_h))
  pred_3d = get_preds_3d(out['hm'].detach().cpu().numpy(),
                         out['depth'].detach().cpu().numpy())[0]

  #pred_3d[6:] = [0,0,0]
  # print(pred_3d)
  debugger = Debugger()
  debugger.add_img(image)
  debugger.add_point_2d(pred, (255, 0, 0))
  debugger.add_point_3d(pred_3d, 'b')
  debugger.show_all_imgs(pause=False)
  debugger.show_3d()
  return pred_3d


def right_arm_gesture(joints, beat):
    rarm = lnd.LabanotationData("right_arm", beat)
    rarm.calculate_symbol(joints[10], joints[11], joints[12])
    return rarm


def left_arm_gesture(joints, beat):
    larm = lnd.LabanotationData("left_arm", beat)
    larm.calculate_symbol(joints[15], joints[14], joints[13])
    return larm

def create_lnd(col, beat, *joints):
    data = lnd.LabanotationData(col, beat)
    data.calculate_symbol(*joints)
    return data

def main(opt):
    opt.heads['depth'] = opt.num_output
    if opt.load_model == '':
        opt.load_model = '../models/fusion_3d_var.pth'
    opt.device = torch.device('cpu')

    model, _, _ = create_model(opt)
    model = model.to(opt.device)
    model.eval()

    # folder = "/Users/nataliapinpin/Documents/HonorsThesisCode/test_videos"
    # img_folder = folder + "/images6"
    # parse_video(folder + "/test6.mov", img_folder)

    file = "4_shorts"
    folder = "/Users/nataliapinpin/Documents/HonorsThesisCode/test_videos/leggings_shorts"
    img_folder = folder + f"/{file}"
    try:
        os.makedirs(img_folder)
    except OSError as exception:
        pass

    parse_video(folder + f"/{file}.mp4", img_folder)

    r_arm_gesture = []
    l_arm_gesture = []
    r_leg_gesture = []
    l_leg_gesture = []
    #if os.path.isdir(opt.demo):
        #ls = os.listdir(opt.demo)
    ls = sorted(os.listdir(img_folder))
    ls.sort(key=lambda img: len(img))
    beat = -1
    for file_name in ls:
        if is_image(file_name):
            image_name = os.path.join(img_folder, file_name)
            print('Running {} ...'.format(image_name))
            image = cv2.imread(image_name)
            preds = get_predictions(image, model, opt)
            beat += 1

            #lnd = right_arm_gesture(preds, beat)
            r_arm = create_lnd("right_arm", beat, preds[10], preds[11], preds[12])
            if len(r_arm_gesture) == 0 or r_arm_gesture[-1] != r_arm:
                r_arm_gesture.append(r_arm)

            l_arm = create_lnd("left_arm", beat, preds[15], preds[14], preds[13])
            # if (len(l_arm_gesture) != 0):
            #     print(l_arm_gesture[-1])
            #     print(l_arm)
            if len(l_arm_gesture) == 0 or l_arm_gesture[-1] != l_arm:
                l_arm_gesture.append(l_arm)

            r_leg = create_lnd("right_leg", beat, preds[0], preds[1], preds[2])
            if len(r_leg_gesture) == 0 or r_leg_gesture[-1] != r_leg:
                r_leg_gesture.append(r_leg)
            #
            l_leg = create_lnd("left_leg", beat, preds[5], preds[4], preds[3])
            if len(l_leg_gesture) == 0 or l_leg_gesture[-1] != l_leg:
                l_leg_gesture.append(l_leg)
                
            # for i in lnd_list:
            #     print(i)
            # print()

    print(len(r_arm_gesture))
    print(len(l_arm_gesture))
    print(len(r_leg_gesture))
    print(len(l_leg_gesture))
    lnd_list = []
    lnd_list.append(r_arm_gesture)
    lnd_list.append(l_arm_gesture)
    lnd_list.append(r_leg_gesture)
    lnd_list.append(l_leg_gesture)
    draw.draw_score(lnd_list,file)



if __name__ == '__main__':
    opt = opts().parse()
    main(opt)