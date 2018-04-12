'''
Created on 2018年1月10日

@author: xmu
'''
# from scipy.io.matlab.tests.test_mio import dtype
'''
Created on 2018年1月3日

@author: xmu
'''
"""
Know more, visit my Python tutorial page: https://morvanzhou.github.io/tutorials/
My Youtube Channel: https://www.youtube.com/user/MorvanZhou
Dependencies:
tensorflow: 1.1.0
matplotlib
numpy
"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from background_program.b_Sample_processing.Feature_calculating import FeatureCalculater


tf.set_random_seed(1)
np.random.seed(1)

# Hyper Parameters
MINIBATCH_SIZE = 100
LR_G = 0.0001  # learning rate for generator
LR_D = 0.0001  # learning rate for discriminator
N_IDEAS = 60  # think of this as number of ideas for generating an art work (Generator)
ART_COMPONENTS = 79  # it could be total point G can draw in the canvas
PAINT_POINTS = np.vstack([np.linspace(-1, 1, ART_COMPONENTS) for _ in range(MINIBATCH_SIZE)])



def get_real_data():  # painting from the famous artist (real target)
    from background_program.a_Data_prossing.DataCarer import DataCarer
    X, Y = DataCarer(label_name='score', school_year='2016', usage="regression").create_train_dataSet()
    X, Y=np.array(X),np.array(Y)
    data = np.hstack((X, Y))
    data = data.astype(float)

#     datamin, datamax =data.min(),data.max() # 求最大最小值
#     data = (data-datamin)/(datamax-datamin) 
#     print(datamin)   
#     print(datamax)         
    result = data
    return result


all_data = get_real_data()

def get_minibatch_data(xdata):
    randomIndex = np.random.randint(len(xdata),size=MINIBATCH_SIZE)
    data = []
    for index in randomIndex :
        data.append(xdata[index])
#         print(data)
    data = np.array(data) 
    datamin,datamax=[],[]
    for i in range(data.shape[1]):
        print(data[0,i])
        max=data[0,i]
        min=data[0,i]
        for j in range(1,data.shape[0]):
            if max<data[j,i]:
                max=data[j,i]
            if min>data[j,i]:
                min=data[j,i]
        if max==min:
            max=1
            min=0

        for z in range(data.shape[0]):
            data[z,i] = (data[z,i]-min)/(max-min)

        datamin.append(min)
        datamax.append(max)
    result= data
#     print(randomIndex)
    return result,datamin,datamax
    
with tf.variable_scope('Generator'):
    G_in = tf.placeholder(tf.float32, [None, N_IDEAS])  # random ideas (could from normal distribution)
    G_l1 = tf.layers.dense(G_in, 128, tf.nn.relu)
    G_out = tf.layers.dense(G_l1, ART_COMPONENTS)  # making a painting from these random ideas

with tf.variable_scope('Discriminator'):
    real_art = tf.placeholder(tf.float32, [None, ART_COMPONENTS], name='real_in')  # receive art work from the famous artist
    D_l0 = tf.layers.dense(real_art, 128, tf.nn.relu, name='l')
    prob_artist0 = tf.layers.dense(D_l0, 1, tf.nn.sigmoid, name='out')  # probability that the art work is made by artist
    # reuse layers for generator
    D_l1 = tf.layers.dense(G_out, 128, tf.nn.relu, name='l', reuse=True)  # receive art work from a newbie like G
    prob_artist1 = tf.layers.dense(D_l1, 1, tf.nn.sigmoid, name='out', reuse=True)  # probability that the art work is made by artist

D_loss = -tf.reduce_mean(tf.log(prob_artist0) + tf.log(1 - prob_artist1))
G_loss = tf.reduce_mean(tf.log(1 - prob_artist1))

# AdamOptimizer 是基于Adam算法的梯度下降算法
train_D = tf.train.AdamOptimizer(LR_D).minimize(
    D_loss, var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Discriminator'))
train_G = tf.train.AdamOptimizer(LR_G).minimize(
    G_loss, var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Generator'))

sess = tf.Session()
# writer = tf.summary.FileWriter('./visual',sess.graph)
sess.run(tf.global_variables_initializer())

plt.ion()  # something about continuous plotting

artist_paintings,datamin,datamax =  get_minibatch_data(all_data)  # real painting from artist
G_ideas = np.random.randn(MINIBATCH_SIZE, N_IDEAS)
G_paintings, pa0, Dl = sess.run([G_out, prob_artist0, D_loss, train_D, train_G],  # train and get results
                                    {G_in: G_ideas, real_art: artist_paintings})[:3]
dataset =FeatureCalculater.FeatureCalculater()
# sql='select score from students_int group by score'
# dataset.executer.execute(sql)
# result = dataset.executer.fetchall()
# for i in result:
#     print(i) 
sql ='truncate gan_float'
dataset.executer.execute(sql)
sql='select count(*) from gan_float'
dataset.executer.execute(sql)

for step in range(100000):
    artist_paintings,datamin,datamax = get_minibatch_data(all_data)  # real painting from artist
#     print(artist_paintings[0])
#     print(len(artist_paintings))
    G_ideas = np.random.randn(MINIBATCH_SIZE, N_IDEAS)
    G_paintings, pa0, Dl = sess.run([G_out, prob_artist0, D_loss, train_D, train_G],  # train and get results
                                    {G_in: G_ideas, real_art: artist_paintings})[:3]

    if step >90010:
#         print('D',tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Discriminator'))
#         print('G',tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Generator'))
 
        lista=[] 
        for i in range(len(G_paintings[0])-1):
            lista.append(abs(G_paintings[0,i]*(datamax[i]-datamin[i])+datamin[i]))
        
        if G_paintings[0,len(G_paintings[0])-1]>99:
            G_paintings[0,len(G_paintings[0])-1]=95
        elif  G_paintings[0,len(G_paintings[0])-1]<30:
            G_paintings[0,len(G_paintings[0])-1]=36
        lista.append(abs(G_paintings[0,len(G_paintings[0])-1]*(datamax[i]-datamin[i])+datamin[i]))
           
        str1=''
        for i in range(0,len(lista)-1):
            str1=str1+str(lista[i])+','
        str1= str1+str(lista[len(lista)-1])    
           
        sql = 'insert into gan_float values({0})'
#         print(str(step)+' '+sql.format(str1))
        dataset.executer.execute(sql.format(str1))
 

sql='select count(*) from gan_float'
dataset.executer.execute(sql)
res=dataset.executer.fetchone()
print(res)

   
# writer.close()
print('程序结束')