'''
Semantic Segmentation Network Evaluation
(Work-In-Progress)
Stand-alone utility to evaluate segmentation predictions using a trained model.
'''

import argparse
import os

from PIL import Image

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import torch.utils.data
import torchvision.transforms as transforms

import utils
from model.segnet import SegNet
from data.dataloaders.SegNetDataLoaderV2 import SegNetDataset

parser = argparse.ArgumentParser(description='PyTorch Semantic Segmentation Evaluation')
parser.add_argument('-j', '--workers', default=0, type=int, metavar='N',
            help='number of data loading workers (default: 4)')
parser.add_argument('--batchSize', default=1, type=int,
            help='Mini-batch size (default: 1)')
parser.add_argument('--bnMomentum', default=0.1, type=float,
            help='Batch Norm Momentum (default: 0.1)')
parser.add_argument('--imageSize', default=256, type=int,
            help='height/width of the input image to the network')
parser.add_argument('--model', default='', type=str, metavar='PATH',
            help='path to latest checkpoint (default: none)')
parser.add_argument('--save-dir', dest='save_dir',
            help='The directory used to save the evaluated images',
            default='save_temp', type=str)
parser.add_argument('--saveTest', default='False', type=str,
            help='Saves the validation/test images if True')

use_gpu = torch.cuda.is_available()

def main():
    global args
    args = parser.parse_args()
    print(args)

    if args.saveTest == 'True':
        args.saveTest = True
    elif args.saveTest == 'False':
        args.saveTest = False

    # Check if the save directory exists or not
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    cudnn.benchmark = True

    data_transform = transforms.Compose([
            transforms.Resize((args.imageSize, args.imageSize), interpolation=Image.NEAREST),
            transforms.ToTensor(),
        ])

    # Data Loading
    data_dir = '/home/ssaserkar/ARCSeg-main/src/data/datasets/cholec'
    # json path for class definitions
    json_path = '/home/ssaserkar/ARCSeg-main/src/data/classes/cholecSegClasses.json'

    image_dataset = SegNetDataset(os.path.join(data_dir, 'test'), data_transform, json_path)

    dataloader = torch.utils.data.DataLoader(image_dataset,
                                             batch_size=args.batchSize,
                                             shuffle=True,
                                             num_workers=args.workers)

    # Get the dictionary for the id and RGB value pairs for the dataset
    classes = image_dataset.classes
    key = utils.disentangleKey(classes)
    num_classes = len(key)

    # Initialize the model
    # TODO: match model initialization code with trainSegNet.py (i.e. model = UNet, ResNetUNet, etc.)
    model = SegNet(args.bnMomentum, num_classes)

    # Load the saved model
    if os.path.isfile(args.model):
        print("=> loading checkpoint '{}'".format(args.model))
        checkpoint = torch.load(args.model)
        args.start_epoch = checkpoint['epoch']
        model.load_state_dict(checkpoint['state_dict'])
        print("=> loaded checkpoint (epoch {})".format(checkpoint['epoch']))
    else:
        print("=> no checkpoint found at '{}'".format(args.model))

    print(model)

    # Define loss function (criterion)
    criterion = nn.CrossEntropyLoss()

    if use_gpu:
        model.cuda()
        criterion.cuda()

    # Initialize an evaluation Object
    evaluator = utils.Evaluate(key, use_gpu)

    # Evaulate on validation/test set
    print('>>>>>>>>>>>>>>>>>>>>>>>Testing<<<<<<<<<<<<<<<<<<<<<<<')
    validate(dataloader, model, criterion, key, evaluator)

    # Calculate the metrics
    print('>>>>>>>>>>>>>>>>>> Evaluating the Metrics <<<<<<<<<<<<<<<<<')
    IoU = evaluator.getIoU()
    print('Mean IoU: {}, Class-wise IoU: {}'.format(torch.mean(IoU), IoU))
    PRF1 = evaluator.getPRF1()
    precision, recall, F1 = PRF1[0], PRF1[1], PRF1[2]
    print('Mean Precision: {}, Class-wise Precision: {}'.format(torch.mean(precision), precision))
    print('Mean Recall: {}, Class-wise Recall: {}'.format(torch.mean(recall), recall))
    print('Mean F1: {}, Class-wise F1: {}'.format(torch.mean(F1), F1))

def validate(val_loader, model, criterion, key, evaluator):
    '''
        Run evaluation
    '''

    # Switch to evaluate mode
    model.eval()

    for i, (img, gt) in enumerate(val_loader):

        # Process the network inputs and outputs
        img = utils.normalize(img, torch.Tensor([0.295, 0.204, 0.197]), torch.Tensor([0.221, 0.188, 0.182]))
        gt_temp = gt * 255
        label = utils.generateLabel4CE(gt_temp, key)
        oneHotGT = utils.generateOneHot(gt_temp, key)

        img, label = Variable(img), Variable(label)

        if use_gpu:
            img = img.cuda()
            label = label.cuda()

        # Compute output
        seg = model(img)
        loss = model.dice_loss(seg, label)

        print('[%d/%d] Loss: %.4f' % (i, len(val_loader)-1, loss.mean().data[0]))

        utils.displaySamples(img, seg, gt, use_gpu, key, args.saveTest, 0, i, args.save_dir)

        evaluator.addBatch(seg, oneHotGT)

if __name__ == '__main__':
    main()
