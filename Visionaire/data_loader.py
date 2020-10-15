# -*- coding: utf-8 -*-
"""EVA_Data_Loader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fj6T8HLiPowkwDvzeVKmf1mHdXA74AWe
"""

import torch 
from torchvision import datasets, transforms
import numpy as np
import os

import albumentations as A
#from albumentations.pytorch import ToTensorV2
from albumentations.pytorch.transforms import ToTensor

from Visionaire import data_albumentations as aug


def MNIST_dataloader(Batch_size, use_cuda ):

    data_transforms = aug.MNIST_Albumentation()
    
    '''
    
    mean =0.1307
    std = 0.3081

    train_transforms = A.Compose([
                                  A.Rotate(limit=90, interpolation=1, border_mode=4, value=None, mask_value=None, always_apply=False, p=0.5),
                                  A.Normalize(
                                      mean= mean,
                                      std=std,
                                      ),
                                  #ToTensorV2()
                                  ToTensor()
                                  ])

   

    # Train Phase transformations
    # train_transforms = transforms.Compose([
    #                                      #  transforms.Resize((28, 28)),
    #                                      #  transforms.ColorJitter(brightness=0.10, contrast=0.1, saturation=0.10, hue=0.1),
    #                                      transforms.RandomRotation((-7.0, 7.0), fill=(1,)),
    #                                      transforms.ToTensor(),
    #                                      transforms.Normalize((0.1307,), (0.3081,)) # The mean and std have to be sequences (e.g., tuples), therefore you should add a comma after the values. 
    #                                      # Note the difference between (0.1307) and (0.1307,)
    #                                      ])
                                        
                                        
    test_transforms = A.Compose([A.Normalize(
                                      mean=mean,
                                      std=std,
                                      ),
                                  ToTensorV2()
                                  ToTensor()
                                  ])

    # Test Phase transformations
    # test_transforms = transforms.Compose([
    #                                      #  transforms.Resize((28, 28)),
    #                                      #  transforms.ColorJitter(brightness=0.10, contrast=0.1, saturation=0.10, hue=0.1),
    #                                      transforms.ToTensor(),
    #                                      transforms.Normalize((0.1307,), (0.3081,))
    #                                      ])
    
    '''


    #Get the MNIST dataset

    train_dataset =  datasets.MNIST('/data/', train=True, download=True,
                              transform= data_transforms(is_train = True) #AlbumentationImageDataset(train_transforms)
                              )


    test_dataset =  datasets.MNIST('/data/', train=False, download=True,
                              transform= data_transforms(is_train = False) #AlbumentationImageDataset(test_transforms)
                              )


    dataloader_args= dict(shuffle=True, batch_size=Batch_size,num_workers=4, pin_memory=True ) if use_cuda else dict(shuffle=True, batch_size=Batch_size)

    train_loader = torch.utils.data.DataLoader(train_dataset, **dataloader_args)

    test_loader = torch.utils.data.DataLoader(test_dataset, **dataloader_args)

    return train_loader,test_loader

def CIFAR10_dataloader(Batch_size, use_cuda,aug_name):

    
    data_preprocess = getattr(aug, aug_name)
    data_transforms = data_preprocess()
    
    #data_transforms = aug.CIFAR10_Albumentation()
    #data_transforms = aug.CIFAR10_A11_transformation() #assignment 11 tranformations
    
    '''

    # mean = [0.4890062, 0.47970363, 0.47680542]
    # std = [0.264582, 0.258996, 0.25643882]



    # # Train Phase transformations Torchvison
    # train_transforms = transforms.Compose([
    #                                       #  transforms.Resize((28, 28)),
    #                                       #  transforms.ColorJitter(brightness=0.10, contrast=0.1, saturation=0.10, hue=0.1),
    #                                       # transforms.RandomRotation((-7.0, 7.0), fill=(1,)),
    #                                       A.HorizontalFlip(p=0.5),
    #                                       A.RandomRotate90()
    #                                       transforms.ToTensor(),
    #                                       transforms.Normalize((0.4890062, 0.47970363, 0.47680542), (0.264582, 0.258996, 0.25643882)) 
    #                                       ])

    # Train Phase transformations Albumentations
    train_transforms = A.Compose([
                                  A.HorizontalFlip(p=0.5),
                                  A.Normalize(
                                      mean= mean,
                                      std=std,
                                      ),
                                  A.Cutout ( num_holes=1, max_h_size=16, max_w_size=16,  fill_value= mean, always_apply=False, p=0.5),
                                  #ToTensorV2()
                                  ToTensor()
                                  ])






    # # Test Phase transformations Torchvision
    # test_transforms = transforms.Compose([
    #                                       #  transforms.Resize((28, 28)),
    #                                       #  transforms.ColorJitter(brightness=0.10, contrast=0.1, saturation=0.10, hue=0.1),
    #                                       transforms.ToTensor(),
    #                                       transforms.Normalize((0.4890062, 0.47970363, 0.47680542), (0.264582, 0.258996, 0.25643882))
    #                                       ])


    # Test Phase transformations Albumentations
    test_transforms = A.Compose([

                                  A.Normalize(
                                      mean=mean,
                                      std=std,
                                      ),
                                  #ToTensorV2()
                                  ToTensor()
                                  ])
                                  
    '''


    #Get the CIFAR10 dataset

    train_dataset =  datasets.CIFAR10('/data/', train=True, download=True,
                              transform= data_transforms(is_train = True) #AlbumentationImageDataset(train_transforms)
                              )


    test_dataset =  datasets.CIFAR10('/data/', train=False, download=True,
                              transform= data_transforms(is_train = False) #AlbumentationImageDataset(test_transforms)
                              )


    dataloader_args= dict(shuffle=True, batch_size=Batch_size,num_workers=4, pin_memory=True ) if use_cuda else dict(shuffle=True, batch_size=Batch_size)

    train_loader = torch.utils.data.DataLoader(train_dataset, **dataloader_args)

    test_loader = torch.utils.data.DataLoader(test_dataset, **dataloader_args)

    classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


    return train_loader,test_loader, classes



def get_id_dictionary():
	
    id_dict = {}
    for i, line in enumerate(open( data_dir + 'wnids.txt', 'r')):
    	id_dict[line.replace('\n', '')] = i

    return id_dict

def get_class_to_id_dict():
    id_dict = get_id_dictionary()
    all_classes = {}
    result = {}
    for i, line in enumerate(open( data_dir + 'words.txt', 'r')):
        n_id, word = line.split('\t')[:2]
        all_classes[n_id] = word
    for key, value in id_dict.items():
        result[value] = (key, all_classes[key])
    return result


def TinyImagenet_dataloader(Batch_size, use_cuda,aug_name):

    data_preprocess = getattr(aug, aug_name)
    data_transforms = data_preprocess()

    data_dir ="S12_Assignment_A/tiny-imagenet-200/"


	   
    #Get the TinyImagenet dataset 

    train_dataset =  datasets.ImageFolder(os.path.join(data_dir, 'train'), train=True, download=True,
                              transform= data_transforms(is_train = True) #AlbumentationImageDataset(train_transforms)
                              )


    test_dataset =  datasets.ImageFolder(os.path.join(data_dir, 'val'), train=False, download=True,
                              transform= data_transforms(is_train = False) #AlbumentationImageDataset(test_transforms)
                              )


    dataloader_args= dict(shuffle=True, batch_size=Batch_size,num_workers=4, pin_memory=True ) if use_cuda else dict(shuffle=True, batch_size=Batch_size)

    train_loader = torch.utils.data.DataLoader(train_dataset, **dataloader_args)

    test_loader = torch.utils.data.DataLoader(test_dataset, **dataloader_args)

    classes = get_class_to_id_dict()


    return train_loader,test_loader, classes