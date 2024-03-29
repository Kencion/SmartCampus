'''
Created on 2018年4月25日

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

class GanB():
    
    def __init__(self):
        # Hyper Parameters
        self.MINIBATCH_SIZE = 100
        self.LR_G = 0.0001  # learning rate for generator
        self.LR_D = 0.0001  # learning rate for discriminator
#         self.PAINT_POINTS = np.vstack([np.linspace(-1, 1, self.ART_COMPONENTS) for _ in range(self.MINIBATCH_SIZE)])
        self.all_data,self.ART_COMPONENTS = self.get_real_data()
        self.N_IDEAS=self.ART_COMPONENTS
        self.final_gan_data=[]
        self.noise=[]
        
    def get_real_data(self):  # painting from the famous artist (real target)
        from background_program.a_Data_prossing.DataCarer import DataCarer
        X, Y = DataCarer(label_name='score', school_year='2016', usage="regression").create_train_dataSet()
        X, Y=np.array(X),np.array(Y)
        data = np.hstack((X, Y))
        data = data.astype(float)    
        result = data
        return result,result.shape[1]
    
    def get_minibatch_data(self,xdata):
        randomIndex = np.random.randint(len(xdata),size=self.MINIBATCH_SIZE)
        data = []
        for index in randomIndex :
            data.append(xdata[index])
        data = np.array(data) 
        datamin,datamax=[],[]
        for i in range(data.shape[1]):
            max=data[0,i]
            min=data[0,i]
            for j in range(1,data.shape[0]):
#                 print(data[j,i])
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
        return result,datamin,datamax

    
    
    
    def run(self):
        tf.set_random_seed(1)
        np.random.seed(1)
        self.final_gan_data.clear()
        
        with tf.variable_scope('Generator'):
            G_in = tf.placeholder(tf.float32, [None, self.N_IDEAS])  # random ideas (could from normal distribution)
            G_l1 = tf.layers.dense(G_in, 512, tf.nn.relu)
            G_l2 = tf.layers.dense(G_l1, 512, tf.nn.sigmoid)
            G_l3 = tf.layers.dense(G_l2, 512, tf.nn.relu)
            G_out = tf.layers.dense(G_l3, self.ART_COMPONENTS)  # making a painting from these random ideas
        with tf.variable_scope('Discriminator'):
            real_art = tf.placeholder(tf.float32, [None, self.ART_COMPONENTS], name='real_in')  # receive art work from the famous artist
            D_l0 = tf.layers.dense(real_art, 512, tf.nn.relu, name='l')
#             D_l2 = tf.
            prob_artist0 = tf.layers.dense(D_l0, 1, tf.nn.sigmoid, name='out')  # probability that the art work is made by artist
            
#           prob_artist01=tf.layers.dense(D_l0[:,-1], 1, tf.nn.sigmoid, name='out2')
            # reuse layers for generator
            D_l1 = tf.layers.dense(G_out, 512, tf.nn.relu, name='l', reuse=True)  # receive art work from a newbie like G
            prob_artist1 = tf.layers.dense(D_l1, 1, tf.nn.sigmoid, name='out', reuse=True)  # probability that the art work is made by artist
            
#             prob_artist11=tf.layers.dense(D_l1[:,-1], 1, tf.nn.sigmoid, name='out2')
        
        D_loss = -tf.reduce_mean(tf.log(prob_artist0) + tf.log(1 - prob_artist1))
        G_loss = tf.reduce_mean(tf.log(1 - prob_artist1))
        
        # AdamOptimizer 是基于Adam算法的梯度下降算法
        train_D = tf.train.AdamOptimizer(self.LR_D).minimize(
            D_loss, var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Discriminator'))
        train_G = tf.train.AdamOptimizer(self.LR_G).minimize(
            G_loss, var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Generator'))
        
        sess = tf.Session()
    # writer = tf.summary.FileWriter('./visual',sess.graph)
        sess.run(tf.global_variables_initializer())
        
        plt.ion()  # something about continuous plotting
        
        for xm in range(self.all_data.shape[0]):
            self.all_data[xm,-1]=self.all_data[xm,-1]*20
        
        for xm in range(self.noise.shape[0]):
            self.noise[xm,-1]=self.noise[xm,-1]*20

        artist_paintings,datamin,datamax =  self.get_minibatch_data(self.all_data)  # real painting from artist
        G_ideas = np.copy(self.noise)
        for i in range(G_ideas.shape[1]):
            for z in range(G_ideas.shape[0]):
                G_ideas[z,i] = abs((G_ideas[z,i]-datamin[i])/(datamax[i]-datamin[i]))
        G_paintings, pa0, Dl = sess.run([G_out, prob_artist0, D_loss, train_D, train_G],  # train and get results
                                            {G_in: G_ideas, real_art: artist_paintings})[:3]
        dataset =FeatureCalculater.FeatureCalculater()
        sql ='truncate gan_float'
        dataset.executer.execute(sql)

        for step in range(60000):
            artist_paintings,datamin,datamax = self.get_minibatch_data(self.all_data)  # real painting from artist
            G_ideas = np.copy(self.noise)
            for i in range(G_ideas.shape[1]):
                for z in range(G_ideas.shape[0]):
                    G_ideas[z,i]= abs((G_ideas[z,i]-datamin[i])/(datamax[i]-datamin[i]))
            G_paintings, pa0, Dl = sess.run([G_out, prob_artist0, D_loss, train_D, train_G],  # train and get results
                                            {G_in: G_ideas, real_art: artist_paintings})[:3]
        
            if step ==59999:
    #         print('D',tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Discriminator'))
    #         print('G',tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Generator'))
#
                for jk in range(len(G_paintings)):
                    lista=[] 
                    for i in range(len(G_paintings[jk])-1):
                        lista.append(abs(G_paintings[jk,i]*(datamax[i]-datamin[i])+datamin[i]))
    #                 
    #                 if G_paintings[0,len(G_paintings[0])-1]>99:
    #                     G_paintings[0,len(G_paintings[0])-1]=95
    #                 elif  G_paintings[0,len(G_paintings[0])-1]<30:
    #                     G_paintings[0,len(G_paintings[0])-1]=36
    #                 
                    lista.append(abs(G_paintings[jk,len(G_paintings[jk])-1]*(datamax[len(G_paintings[jk])-1]-datamin[len(G_paintings[jk])-1])+datamin[len(G_paintings[jk])-1]))
                    self.final_gan_data.append(lista.copy())  
                               
    #                 str1=''
    #                 for i in range(0,len(lista)-1):
    #                     str1=str1+str(lista[i])+','
    #                 str1= str1+str(lista[len(lista)-1])    
    #                     
    #                 sql = 'insert into gan_float_2 values({0})'
    #                 print(str(step)+' '+sql.format(str1))
    #                 print(sql.format(str1))
    #                 dataset.executer.execute(sql.format(str1))
                self.final_gan_data=np.array(self.final_gan_data)
                print(self.final_gan_data[:,-1]) 
        self.final_gan_data=np.array(self.final_gan_data)
        
        sess.close()
        print('Gan结束')

if __name__ =='__main__':
    ts=GanB()
    ts.run()
    print(ts.final_gan_data[:,-1])