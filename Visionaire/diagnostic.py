# -*- coding: utf-8 -*-
"""EVA_Utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10WBfOzz1_ZuleuZih9nWgkEtMwCX22AV
"""

# Commented out IPython magic to ensure Python compatibility.
import torch 
import torch.nn as nn
import torchvision
from torchsummary import summary
import torch.nn.functional as F
import torch.optim as optim
#%matplotlib inline
import matplotlib.pyplot as plt

from torchvision import transforms

import numpy as np


'''
#data Statistics
train = train_dataset.train_data
train = train_dataset.transform(train.numpy())


print("Train data statistics : ")

print('#    Numpy shape :' ,train.numpy().shape)
print('#    Tensor shape :', train_dataset.train_data.size())
print('#    Max :', torch.max(train))
print('#    min :', torch.min(train))
print('#    std:', torch.std(train))
print('#    var:', torch.var(train))
print('#    Mean:', torch.mean(train))
'''

def incorrect_images(model, device, test_loader):
  incorrect_examples = []  ## store incorrect images
  incorrect_target = []
  incorrect_pred =[]

  model.eval()
  test_loss=0
  correct=0
  with torch.no_grad():
    for data, target in test_loader:
      data, target = data.to(device), target.to(device)
      output = model(data)
      #test_loss += F.nll_loss(output, target, reduction='sum').item()
      pred = output.data.max(1, keepdim=True)[1]
      correct += pred.eq(target.data.view_as(pred)).sum().item()
      
      idxs_mask = (pred.eq(target.data.view_as(pred))==False).nonzero(as_tuple=False) ## store incorrect images

      for id in idxs_mask:
        incorrect_examples.append(data[id[0].item()])
        incorrect_target.append(target[id[0].item()].item())
        incorrect_pred.append(pred[id[0].item()].item())

  incorrect={'images':incorrect_examples,
             'Pred':incorrect_pred,
             'target':incorrect_target}

  return incorrect




def incorrect_Classification(model,classes,test_loader,device, savefig = False, *save_dir):


  incorrect = incorrect_images(model, device, test_loader)
  incorrect_examples = incorrect['images']
  incorrect_pred = incorrect['Pred']
  incorrect_target = incorrect['target']

  inv_normalize = transforms.Normalize(
    mean=[-0.4890062/0.264582, -0.47970363/0.258996, -0.47680542/0.25643882],
    std=[1/0.264582, 1/0.258996, 1/0.25643882]
  )


  #fig = plt.figure(figsize=(15,10))
  fig,ax = plt.subplots(nrows = 5, ncols = 5,figsize=(15,10))

  for i in range(25):
    plt.subplot(5,5,i+1)
    #plt.tight_layout(pad=0, w_pad=0, h_pad=0.4)
    #incorrect_examples_inv = inv_normalize(incorrect_examples[i])

    incorrect_examples_temp = inv_normalize(incorrect_examples[i])
    incorrect_examples_temp = incorrect_examples_temp.cpu().numpy()

    plt.imshow((np.transpose(incorrect_examples_temp, (1, 2, 0)).squeeze() *255).astype(np.uint8))
    plt.title(f"Predicted:{classes[incorrect_pred[i]]} \n Target:{classes[incorrect_target[i]]}",color='red',fontsize=16)
    plt.axis('off')
    plt.tight_layout()

  if savefig:
    plt.savefig(save_dir[0]+'incorrect_images.jpg', dpi=300, bbox_inches='tight')

  plt.show()
  
  
def plot_performace(train_acc,test_acc,train_losses,test_losses,savefig = False, *save_dir):

    fig, axs = plt.subplots(1,2,figsize=(10,5))
    axs[0].plot(train_losses,label = "Train")
    axs[0].plot(test_losses,label = "Test")
    axs[0].legend()
    axs[0].set_title("Loss curve",color='red')
    axs[0].set_xlabel('Epochs')
    axs[0].set_ylabel('Loss')

    axs[1].plot(train_acc,label = "Train")
    axs[1].plot(test_acc,label = "Test")
    axs[1].set_title("Accuracy curve",color='red')
    axs[1].legend()
    axs[1].set_xlabel('Epochs')
    axs[1].set_ylabel('Accuracy %')

    plt.tight_layout()
    
    if savefig:
        plt.savefig(save_dir[0]+'model_performance.jpg', dpi=300, bbox_inches='tight')
    
    plt.show()
    
    
def class_accuracy(classes,model,test_loader,device):
  num_class = len(classes)
  class_correct = list(0. for i in range(num_class))
  class_total = list(0. for i in range(num_class))
  with torch.no_grad():
    for data in test_loader:
      images, labels = data
      images, labels = images.to(device), labels.to(device)
      outputs = model(images)
      _, predicted = torch.max(outputs, 1)
      c = (predicted == labels).squeeze()
      for i in range(4):
        label = labels[i]
        class_correct[label] += c[i].item()
        class_total[label] += 1
  
  for i in range(num_class):
    print('Accuracy of %5s : %2d %%' % (
            classes[i], 100 * class_correct[i] / class_total[i]))
 