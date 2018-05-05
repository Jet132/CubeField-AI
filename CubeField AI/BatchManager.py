from numpy import append,array
from PIL import Image
from random import randint

file_names = [[],[],[]]

def load_dataset():
    file_names[0] = [line.rstrip('\n') for line in open("data 0.txt")]
    file_names[1] = [line.rstrip('\n') for line in open("data 1.txt")]
    file_names[2] = [line.rstrip('\n') for line in open("data 2.txt")]
    print('finished loading names')
            

def get_Batch(lenght):
    images = [[] for i in range(lenght)]
    labels = [[] for i in range(lenght)]
    for i in range(lenght):
        control = randint(0,2)
        index = randint(0,len(file_names[control])-1)
        label = []
        if(control == 0):
            label = append(label,[1,0,0])
        elif(control == 1):
            label = append(label,[0,1,0])
        else:
            label = append(label,[0,0,1])
        labels[i] = label
        images[i] = array(Image.open('data/'+file_names[control][index]))
    #print('loaded batch')
    return array(images),array(labels)