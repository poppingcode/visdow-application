#  _*_ coding:utf-8 _*_ 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import torch
from visdom import Visdom
import numpy as np
import math
import os.path
import getpass
from sys import platform as _platform
from six.moves import urllib
import numpy as np
viz = Visdom(env=u'sth_sth_train_loss_fromysd')
#assert viz.check_connection()
viz.close()

##首先是建立一个wienv=u'test'n, 下面建立了一个曲线的win
win=viz.line(
    X=torch.FloatTensor([0,0]),
    Y=torch.FloatTensor([0,0]),
    name="Prec_train",
    opts={'title': 'rgb_train_loss'}
)

viz.line(
    X=torch.FloatTensor([0,0]),
    Y=torch.FloatTensor([0,0]),
    name="Prec_test",
    #update="new",
    opts={'title': 'rgb_train_Prec'}
)

input = open('sth-sth.log', 'r')
epoch = []
epoch_test = []
loss = []
prec = []
test_prec = [] 
n = 0;
for line in input:
    line = line.split()
    if 'Epoch:' in line:
        loss.append(float(line[11]))
        prec.append(float(line[14]))
        zline = line[1].split("]")     #line[1] = [0][0/660]
        tline = zline[0].split("[")#分离出第几个epoch整数部分epoch
        awline = zline[1].split("[")#分离出第几个epoch小数部分epoch
        bwline = awline[1].split("/")
        wline = float(bwline[0])/float(bwline[1])
        epoch.append(float(tline[1])+wline)
    if 'Test:' in line:
        #n = n+1
        test_prec.append(float(line[9]))
        zline1 = line[1].split("]")     #line[1] = [0][0/660]
        tline1 = zline1[0].split("[")#分离出第几个epoch整数部分epoch
       # awline1 = tline1[1].split("[")#分离出第几个epoch小数部分epoch
        bwline1 = tline1[1].split("/")
        wline1 = float(5*int(n/10)+5) + (float(bwline1[0])/float(bwline1[1]))
        print(wline1)
        n = n+1
        epoch_test.append(wline1)
#print(loss[1])
#print(epoch[1])
for j in range(len(epoch_test)):
    Epoch = epoch_test[j] 
    Prec = test_prec[j]   
    viz.line(
        X=torch.FloatTensor([Epoch]),
        Y=torch.FloatTensor([Prec]),
        win=win,
        name="Prec_test",
        update = 'append'
    )

for i in range(len(epoch)):
    Epoch = epoch[i]
    #Loss = loss[i]
    Prec = prec[i]
    viz.line(
        X=torch.FloatTensor([Epoch]),
        Y=torch.FloatTensor([Prec]),
        win=win,
        name="Prec_train",
        update = 'append'
    )


