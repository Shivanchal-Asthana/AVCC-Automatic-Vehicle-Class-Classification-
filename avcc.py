#!/usr/bin/python3

#import necessary libraries

'''Tkinter Library'''
from tkinter import Button,Canvas,Tk,Label,Message,Scrollbar,Frame,filedialog,ttk
from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkinter import ttk

'''Serial Library'''
import serial
import serial.tools.list_ports
from serial import Serial

'''Datetime Library'''
import datetime as dt
from datetime import datetime, date

'''PIL Library'''
from PIL import ImageDraw, ImageOps, ImageEnhance
import PIL.Image
import PIL.ImageTk
from PIL.ImageFilter import*

##from PIL.ImageFilter import (BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
##   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN)

'''import Threading'''
import threading
from threading import Thread
from _thread import *

'''opencv Library'''
import cv2

'''os library'''
import os
from os import listdir

'''socket Library'''
import socket

'''Other libraries'''
import io
import sys
import time
import shutil
import pickle
import base64
import traceback
import numpy as np
from array import *
import pandas as pd
import scipy.ndimage

'''import warnings'''
import warnings
warnings.filterwarnings("ignore")

#initializing variables
counter=k=0
Number_of_axle=u3=u4=u5=h11=n1=0
v=v1=v2=v3=v4=v5=v6=acc=gen_str=0
max_value = None

#creating empty list
img,one_list,Number_of_axles,vehicle_hgt,date1,sort_date=[],[],[],[],[],[]

''' ################ Initialize serial port #####################'''

serialobj = serial.Serial()
serialobj.port = "/dev/ttyAMA0"
serialobj.baudrate= 115200
serialobj.open()

try:
    ob=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #ob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    ob.bind(('192.168.1.220', 5000))
    ob.listen(5)
except OSError:
    pass

clients = set()
clients_lock = threading.Lock()

'''############## access current count value from text file 'count'############### '''
#initialze count variable
j=0
if os.path.exists('/home/tollman/AVC/count.txt'):  #Create text file if not exist
    pass
else:
    try:
        with open('/home/tollman/AVC/count.txt', 'w') as f: #if file not exist, then write count 1 into it
            f.write(str('0'))
    except:
        pass
f = open('/home/tollman/AVC/count.txt', 'r')
j = int(f.read()) #read the current number
j = j + 1

time.sleep(5)
''' ################### Starting the GUI ######################'''
root = Tk()
root.config(bg='gray')
root.geometry('780x500')
root.title("AVC Independent Profiler Software")


''' ################### Creating another canvas for showing images ######################'''
canvas = tk.Canvas(root, width=780, height=300, bg="white")
canvas.pack()

string_frame1 = Frame(root, width=700, height=200,bg="orange")
string_frame1.pack(fill=X)

''' ################### Creating 'Canvas' for showing the string of the vehicle ######################'''
datacanvas = Canvas(string_frame1, width = 400, height = 200, bg = 'white')
datacanvas.pack(side=LEFT,fill=BOTH,padx=10, pady=10)

''' ################### Creating a scrollbar for string data in canvas ######################'''
vsb = Scrollbar(string_frame1, orient = 'vertical', command = datacanvas.yview,background="orange",
    elementborderwidth=1,bd=2, takefocus=0, troughcolor='#ffad33', width=17)
vsb.pack(side=LEFT, fill=Y)

datacanvas.config(yscrollcommand = vsb.set)
dataframe = Frame(datacanvas, bg='white')
datacanvas.create_window((5,0),window=dataframe, anchor='nw')

''' ######################  Creating Label as a heading for the 'Vehicle Class' ###########################'''
label = Label(string_frame1, text="Vehicle Class", width=40, height=2, bg = "#ffad33", font=('Arial', 17, 'bold')) 
label.pack(side=RIGHT, anchor='nw', padx=7, pady=8)

''' ################### Creating 'Message Box' to show the class of the vehicle ######################'''
message_font = font.Font(size=16)
mesg = Message(string_frame1, text="No vehicle!!", font= message_font, justify = tk.CENTER, width = 180)  
mesg.place(x=455, y=70, width=315, height=115, bordermode= OUTSIDE)
mesg.config(bg='white')


''' ################### function for convert string data into images ######################'''
d=[]
def binary_fn(str2,j):
    L1,line1=[],[]
    try:
        sliced_str = str2[0:29]
        try:
            if len(sliced_str)==29:
                result = bin(int(sliced_str,16))
                c = result[6:]
                c_1 = list(c)
                d.append(c_1)
                arr = np.array(d, ndmin=2)
                arr = arr.transpose()
                L1 = arr.tolist()
                for i, line in enumerate (L1):
                    line = [int(x) for x in line]
                    if sum(line)!=0:
                        line1.append(line)   
                arr1 = np.array(line1, ndmin=2)
                arr1 = arr1.astype('uint8')*255
                arr1 = cv2.rotate(arr1, cv2.ROTATE_180)
                try:
                    (height, width) = arr1.shape[:2]
                    if width<50:
                        arr1 = cv2.resize(arr1, (width*10, 150))
                    elif width>=50 and width<80:
                        arr1 = cv2.resize(arr1, (width*6, 150))
                    elif width>=80 and width<100:
                        arr1 = cv2.resize(arr1, (width*4, 150))
                    elif width>=100 and width<120:
                        arr1 = cv2.resize(arr1, (width*3, 150))
                    elif width>=120 and width<140:
                        arr1 = cv2.resize(arr1, (width*4, 150))
                    elif width>=150:
                        arr1 = cv2.resize(arr1, (width*3, 150))
                    kernel = np.ones((1,1), np.uint8)
                    _, th1 = cv2.threshold(arr1, 100,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                    c1 = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
                    mask_inv = cv2.bitwise_not(c1)
                    mask_inv = cv2.flip(mask_inv, 1)
                    c = ''.join(c)
                    save_image(mask_inv,j)
                    axle_number(c)
                except AttributeError:
                    pass
            else:
                Label(dataframe, text = "Data Lost issue", font = ('calibri','13'), bg='white').pack()
                root.update()
        except PermissionError:
            pass
    except ValueError:
        pass

def image_clear(c):
    c_2 = list(c)
    c_3 = c_2.index('1')
    if c_3 == 0:
        c_4 = c_2.index('0')
        if c_4 < 10:
            c_5 = c.replace('1','0')
            return c_5
''' ################### Function for saving the images ######################'''
def save_image(mask_inv,j):
    #****************Black Image*********************
    cv2.imwrite('/home/tollman/AVC/image.png',mask_inv)

''' ################### Function for colorize the images ######################'''
def color_image(j):
    fp = open("/home/tollman/AVC/image.png","rb")
    img = PIL.Image.open(fp).convert("L")
    img_1 = ImageOps.colorize(img, black = "orange", white ="white")
    img_2 = ImageEnhance.Sharpness(img_1)
    img_3 = img_2.enhance(8.0)
    save_to_folder(img_3,j)
    
newData = []
''' ################### Function for saving the images in particular folder ######################'''    
def save_to_folder(img_3,j):
    directory_path_main='/home/tollman/AVC/'
    directory_name_main='Images/'

    try:
        path_1 = os.path.join(directory_path_main,directory_name_main)
        os.makedirs(path_1, exist_ok=True)
    except OSError as error:
        pass
    
    td1 = dt.datetime.now()
    directory_name_1 = str(td1.year)
    try:
        path_2 = os.path.join(path_1,directory_name_1)
        os.makedirs(path_2, exist_ok = True)
    except OSError as error:
        pass
    directory_name_2 = td1.strftime("%B")
    try:
        path_3 = os.path.join(path_2,directory_name_2)
        os.makedirs(path_3, exist_ok = True)
    except OSError as error:
        pass
    directory_name_3 = td1.strftime("%d-%m-%Y") 
    img1 = img_3.convert("RGBA")
    datas = img1.getdata()

    for item in datas:
        if item[0] >= 250 and item[1] >= 250 and item[2] >= 250:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img1.putdata(newData)
    ImageDraw.floodfill(img1,xy=(0,0),value=(255,0,255),thresh=10)

    try:
        path_4 = os.path.join(path_3,directory_name_3)
        os.makedirs(path_4, exist_ok = True)
        new_file_path = os.path.join(path_4, str(j)+'.png')
        img1.save(new_file_path,"PNG")
        open_image_gui(j)
    except OSError as error:
        pass

''' ################### Function for opening the saved image on GUI ######################'''
def open_image_gui(j):
    try:
        fp = open("/home/tollman/AVC/image.png","rb")
        root.img = img = PIL.Image.open(fp).convert("L")
        img = img.resize((600,200), PIL.Image.Resampling.LANCZOS)
        img_4 = ImageOps.colorize(img, black = "#ff9900", white ="white")
        img_5 = ImageEnhance.Sharpness(img_4)
        img_6 = img_5.enhance(12.0)
        img_7 = img_6.filter(DETAIL)
        try:
            imgtk = PIL.ImageTk.PhotoImage(image=img_7)
        except AttributeError:
            pass
        canvas.image = imgtk # keep a reference!
        canvas.create_image((410,130), anchor='center',image=imgtk)
        canvas.update()
        get_data(j)
    except (RuntimeError, AttributeError):
        pass

''' ################### Function for counting the total axle of particluar vehicle ######################'''
def axle_number(c):
    global k, Number_of_axle
    count_1 = sum(map(lambda x : 1 if '1' in x else 0, c))
    if c.startswith('1'):
        k+=1
        one_list.append(str(k))
    elif c.startswith('0'):
        k=0
    if count_1<50:
        Number_of_axles.append(one_list.count('3'))
    else:
        Number_of_axles.append(one_list.count('4'))
    axle = Number_of_axles[-1:][0]
    Number_of_axle = str(axle)
    first_two_axle_height(c,axle)

''' ################### Function for calculating the height of the first two axle of vehicle ######################'''
u,u1,u2=[],[],[]
def first_two_axle_height(c,axle):
    global u3,u4,u5,u1,u2,u
    try:
        if c.startswith('1'):
            c = list(c)
            sec = [x for x in range(len(c)) if c[x] == '1']
            u.append(sec[-1])
        elif c.startswith('0'):
            if u==0:
                pass
            elif u!=0:
                if u==[]:
                    pass
                elif u!=[]:
                    u2.append(min(u)+1)
                    u1.append(max(u)+ 1)
                    for i in range (len(u1)):
                        if i == 0:
                            u3= u1[0]
                            u4 = u2[0]
                        elif i==1:
                            u5 = u1[1]
                        u.clear()
        vehicle_height(c, axle)
    except IndexError:
        pass

''' ################### Function for calculating the height of the vehicle ######################'''
h12=[]
def vehicle_height(c,axle):
    global h11
    try:
        c = list(c)
        res = [x for x in range(len(c)) if c[x] == '1']
        res = res[-1]
        h12.append(res)
        h12.sort()
        h11 = str(max(h12)+1)
        axle_distance(c,axle)
    except IndexError:
        pass
''' ################### Function for calculating the distance of first two axle of vehicle ######################'''
m=0
n=[]
def axle_distance(c,axle):
    global m
    try:
        c = list(c)
        if c[0]=='1':
            if c.count('1')>20:
                m+=1
            elif c.count('1')<10:
                m=0
                n.append(m)
        elif c[0]=='0':
            n.append(m)
            m=0
        ground_clearance(c, axle)
    except IndexError:
        pass

''' ################### Function for ground clearance ######################'''
w,w1=[],[]
def ground_clearance(c, axle):
    global v,v1,v2,v3,v6
    try:
        c = list(c)
        gnd = [x for x in range(len(c)) if c[x] == '1']
        gnd = gnd[0]
        if gnd!=0:
            w.append(gnd)
        else:
            if w!=[]:
                v1 = w[1:]
                v4=w[2:]
                if v1!=[]:
                    if axle == 1:
                        for i in v1:
                            if i<12:
                                v2+=1
                            else:
                                v3+=1
                if v4!=[]:
                    v5 = v4[:-2]
                    v6 = sum(x>4 and x<10 for x in v5)
        Number_of_windows(c,axle)
    except IndexError:
        pass

''' ################### Function for calculating the window on second axle ######################'''
''' This function is specially to check the window on second axle of bus, only used to differentiate
between 2 Axle Truck and Bus'''
windows,win=[],[]
def Number_of_windows(c, axle):
    try:
        c = list(c)
        if c[0]=='1':
            windows.append(c.count('1'))
        elif c[0]=='0':
            win.append(windows[-2])
            windows.clear()
    except IndexError:
        pass
    windows_horizontal(c,axle)

''' ################### Function is calculating all windows of bus ######################'''
windows_counter=0
def windows_horizontal(c,axle):
    global h11,windows_counter
    string_value = ''.join(c)
    string_value1 = int(int(h11)/2)
    string_value3 = int(h11)
    string_value2 = string_value[string_value1:string_value3]
    if string_value2.count('0') > 10:
        windows_counter+=1
    else:
        pass
    tandum_axle(c,axle)

bin_img_3 = []
bin_img_4 = []
bin_img_5 = []
bin_img_6 = []
def tandum_axle(c,axle):
    global tandum_axle_status
    bin_img = ''.join(c)
    if 1<axle<4:
        if bin_img.startswith('0'):
            bin_img_1 = bin_img[:12]
            bin_img_2 = bin_img_1.count('1')
            bin_img_3.append(bin_img_2)
            bin_img_4 = [i for i in bin_img_3 if i != 0 and i != 1]
            bin_img_5 = [i<j for i, j in (zip(bin_img_4, bin_img_4[1:]))]
            bin_img_6 = [a>b for a, b in (zip(bin_img_4, bin_img_4[1:]))]
            res_acc = [element for m, element in enumerate(bin_img_5) if element == 1][0]
            res_dec = [element for n, element in enumerate(bin_img_6) if element == 1][0]
            if res_acc == res_dec:
                tandum_axle_status = res_acc
            else:
                tandum_axle_status = 0
                
            
def delete_folder():
    path = "/home/tollman/AVC/images/"
    days = 90
    seconds = time.time() - days*60*60
    if os.path.exists(path):
        for j,folder in enumerate(os.listdir(path)):
            if j == 0:
                if os.path.exists(path):
                    path_1 = path + ''.join(os.listdir(path)[0])
                    dir = os.listdir(path_1)
                    if len(dir)==0:
                        if j == 0:
                            shutil.rmtree(path_1)
                    else:
                        for i, filename in enumerate(os.listdir(path_1)):
                            concatenate_path = path_1+str('/') + filename
                            ctime = os.stat(concatenate_path).st_ctime
                            if seconds > ctime:
                                if i<3:
                                    shutil.rmtree(concatenate_path)

thread7 = threading.Thread(target = delete_folder, daemon = True).start()


def delete_str_folder():
    path = "/home/tollman/AVC/String_file/"
    days = 90
    seconds = time.time() - days*60*60
    if os.path.exists(path):
        for j,folder in enumerate(os.listdir(path)):
            if j == 0:
                if os.path.exists(path):
                    path_1 = path + ''.join(os.listdir(path)[0])
                    dir = os.listdir(path_1)
                    if len(dir)==0:
                        if j == 0:
                            shutil.rmtree(path_1)
                    else:
                        for i, filename in enumerate(os.listdir(path_1)):
                            concatenate_path = path_1+str('/') + filename
                            ctime = os.stat(concatenate_path).st_ctime
                            if seconds > ctime:
                                if i<3:
                                    shutil.rmtree(concatenate_path)

thread7 = threading.Thread(target = delete_str_folder, daemon = True).start()

''' ################### Function is saving string data into text file ######################'''    
def text_data(j, recentpacket):
    td1 = dt.datetime.now()
    td = td1.strftime("%d-%m-%Y")
    directory_path_str_1='/home/tollman/AVC/'
    directory_name_main_1='String_file'
    try:
        path_str_1 = os.path.join(directory_path_str_1,directory_name_main_1)
        os.makedirs(path_str_1, exist_ok=True)
    except OSError as error:
        pass
    td1 = dt.datetime.now()
    directory_name_1 = str(td1.year)
    try:
        path_str_2 = os.path.join(path_str_1,directory_name_1)
        os.makedirs(path_str_2, exist_ok = True)
    except OSError as error:
        pass
    directory_name_2 = td1.strftime("%B")
    try:
        path_str_3 = os.path.join(path_str_2,directory_name_2)
        os.makedirs(path_str_3, exist_ok = True)
    except OSError as error:
        pass
    directory_name_3 = td1.strftime("%d-%m-%Y") 
    try:
        path_str_4 = os.path.join(path_str_3,directory_name_3)
        os.makedirs(path_str_4, exist_ok = True)
        new_file_path = os.path.join(path_str_4, str(j)+'.txt')
        new_file = open(new_file_path,'a')
        new_file.writelines(str(recentpacket))
        new_file.writelines('\n')
        new_file.close()
    except OSError as error:
        pass

''' ################### Function is clearing the string data on canvas ######################'''
clear_counter=0 
def clear_frame():
    global dataframe
    for widgets in dataframe.winfo_children():
        widgets.destroy()

''' ################### Function is reading the string data by serial port ######################'''
def checkSerialPort():
    global counter,j, clear_counter
    compare_list=['A00FFFFFFFFFFFFFFFFFFFFFFFFFF;,0\r']
    try:
        if serialobj.isOpen() and serialobj.in_waiting:
            recentpacket = serialobj.readline()
            text_data(j, recentpacket)
            recentpacketstring = recentpacket.decode('utf').rstrip('\n')
            str1 = ''+ recentpacketstring
            compare_list.append(str1)
            if str1.startswith("A"):
                try:  #for loop for copying the unnecessary data
                    for i in range(len(compare_list)):
                            if compare_list[i] == compare_list[i+1]:
                                Label(dataframe, text = 'No vehicle', font = ('calibri','13'), bg='white').pack()
                                root.update()
                                compare_list.clear()
                                
                            else:
                                Label(dataframe, text = str1, font = ('calibri','13'), bg='white').pack()
                                str2 = ''+ recentpacketstring
                                binary_fn(str2,j)        
                except IndexError:
                    pass   
            elif str1.startswith("S"):
                color_image(j)
                j+=1
                Number_of_axle=u3=u4=u5=h11=n1=v2=v3=0
                first_two_axle_distance, v6= 0,0
                tandum_axle_status=0
                d.clear()
                Number_of_axles.clear()
                one_list.clear()
                vehicle_hgt.clear()
                n.clear()
                w.clear()
                u.clear()
                u1.clear()
                u2.clear()
                h12.clear()
                win.clear()
                axle_dist.clear()
                newData.clear()
                newData_1.clear()
                bin_img_3.clear()
                bin_img_4.clear()
                bin_img_5.clear()
                bin_img_6.clear()
                tandum = 'False'
                tandum_axle_status=0
            else:
                Label(dataframe, text = 'No Vehicle', font = ('calibri','13'), bg='white').pack()
                root.update()
                pass
        else:
            clear_counter+=1
            if clear_counter>1500:
                clear_frame()
                clear_counter=0
    except UnicodeDecodeError:
        pass

''' ################################ Classification function  #############################'''
#Initializing Lists
nwlist,ax_ht,both_axle_counts,axle_dist=[],[],[],[]
#Global variables
tandum='False'
tandum_axle_status = 0
max_value = None
Number_of_axle,u3,u4,u5,h11,n,v2,v3,v6, windows_counter

def get_data(j):
    global max_value, ad, Number_of_axle,tandum, u3,u4,u5,h11,n,v2,v3,v6,win, windows_counter,tandum_axle_status
    Number_of_axle = str(Number_of_axle)
    delete_folder()
    delete_str_folder()
    try:
        len_n = len(n)
        for i in range (len_n):
            if (n[i] != 0 and n[i] != 1):
                axle_dist.append(i)
        first_two_axle_distance = axle_dist[1]-axle_dist[0]
        first_two_axle_distance = int(first_two_axle_distance)*3
    except:
        first_two_axle_distance=0
    v6 = int(v6)
    axle_ht1 = int(u4)*3
    axle_ht2 = int(u3)*3
    max_hgt = int(h11)*3
    sec_ax_ht1 = int(u5)*3
    gnd_clr_OFF = int(v2)*3
    gnd_clr_ON = int(v3)*3
    try:
        windows = win[-1]
        windows1 = int(windows)
    except:
        windows1 = 0
    axle_ht=ttl_hgt=sec_ax_ht=windows=v2=v3=0 
    try:
        # Loop for number of axle is zero
        if Number_of_axle == '0':
            if axle_ht1<130 and max_hgt>100 and gnd_clr_ON<40:
                txt = '3,CJV'
                message_box(txt)
                Number_of_axle=2
            else:
                txt='0,Non Tollable'
                message_box(txt)
        # Loop for number of axle is one
        elif Number_of_axle == '1':
            if 70<axle_ht1<130  and  70<sec_ax_ht1<270 and gnd_clr_ON<40:
                txt = '3,CJV'
                Number_of_axle=2
                message_box(txt)
            elif 70<axle_ht1<130  and gnd_clr_ON<40:
                txt = '3,CJV'
                Number_of_axle=2
                message_box(txt)
            else:
                txt='0,Non Tollable'
                message_box(txt)
        # Loop for number of axles are two
        elif Number_of_axle == '2':
            if axle_ht1<50 and 10<gnd_clr_ON<40:
                txt = '2,3 Wheeler'
                message_box(txt)
            elif 115<axle_ht1<130 and 20<gnd_clr_ON<30:
                txt = '12,Tractor'
                message_box(txt)
            elif axle_ht1<130  and  70<sec_ax_ht1<260 and gnd_clr_ON<30:
                txt = '3,CJV'
                message_box(txt)
            elif axle_ht1<130  and  60<axle_ht2<150 and gnd_clr_ON<gnd_clr_OFF:
              txt = '3,CJV'
              message_box(txt)
            elif axle_ht1<130  and  60<axle_ht2<150 and gnd_clr_ON>gnd_clr_OFF:
              txt = '3,CJV'
              message_box(txt)
            elif axle_ht1<250:
                txt = '4,LCV'
                message_box(txt)
            elif axle_ht1>235 and sec_ax_ht1-axle_ht1>13:
                if gnd_clr_ON<gnd_clr_OFF:
                    txt = '6,BUS'
                    message_box(txt)
                else:
                    txt = '4,LCV'
                    message_box(txt)
            elif 250<axle_ht1<265 and 250<sec_ax_ht1<280 and gnd_clr_ON<gnd_clr_OFF: 
                txt = '6,BUS'
                message_box(txt)
            elif axle_ht1>260 and gnd_clr_ON<gnd_clr_OFF:
                if axle_ht1>260 and windows_counter>13:
                    txt = '6,BUS'
                    message_box(txt)
                elif axle_ht1>260 and windows1 < 100:
                    txt = '6,BUS'
                    message_box(txt)
                else:
                    txt = '7,2 Axle Truck'
                    message_box(txt)
            elif axle_ht1>300 and gnd_clr_ON>gnd_clr_OFF:
                if windows1>100:
                    txt = '7,2 Axle Truck'
                    message_box(txt)
                elif axle_ht1>300 and max_hgt> 325 and windows_counter<50:
                    txt = '7,2 Axle Truck'
                    message_box(txt)
                elif axle_ht2> 270 and axle_ht1-sec_ax_ht1>10:
                    txt = '7,2 Axle Truck'
                    message_box(txt)
                elif max_hgt> 270 and axle_ht1-sec_ax_ht1>10:
                    txt = '7,2 Axle Truck'
                    message_box(txt)
                else:
                    txt = '6,BUS'
                    message_box(txt)
            elif max_hgt> 270 and axle_ht1-sec_ax_ht1>15:
                txt = '7,2 Axle Truck'
                message_box(txt)
            elif max_hgt> 300 and axle_ht2-axle_ht1>15:
                txt = '7,2 Axle Truck'
                message_box(txt)
            else:
                txt = '6,BUS'
                message_box(txt)
        # Loop for number of axles are three
        elif Number_of_axle == '3':
            if axle_ht1<130  and sec_ax_ht1<270 and gnd_clr_ON<25:
                txt = '3,CJV'
                message_box(txt)
                Number_of_axle=2
            elif 100<axle_ht1<150:
                txt = '13,Tractor Trolley'
                message_box(txt)
            elif axle_ht1>250 and gnd_clr_ON<gnd_clr_OFF:
                txt = '6,BUS'
                message_box(txt)
            elif axle_ht1>250 and gnd_clr_ON>gnd_clr_OFF:
                if tandum_axle_status == 1:
                    tandum = 'True'
                    txt = '8,3 Axle Truck'
                    message_box(txt)
                else:
                    txt = '8,3 Axle Truck'
                    message_box(txt)

            else:
                txt = '8,3 Axle Truck'
                message_box(txt)
        # Loop for number of axles are between 3 and 6
        elif Number_of_axle > '3' and Number_of_axle <= '6':
            if axle_ht1<130  and  sec_ax_ht1<270 and gnd_clr_ON<40:
                txt = '3,CJV'
                message_box(txt)
                Number_of_axle=2
            elif axle_ht1<160:
                txt = '13,Tractor Trolley'
                message_box(txt)
            elif tandum_axle_status == 1:
                tandum = 'True'
                txt = '9,MAV'
                tandum_axle_status=0
                message_box(txt)
                v6=0
            else:
                txt = '9,MAV'
                message_box(txt)
        # Loop for number of axles are more than 6
        elif Number_of_axle > '6':
            if 70<axle_ht1<130  and  70<sec_ax_ht1<270 and gnd_clr_ON<40:
                txt = '3,CJV'
                message_box(txt)
                Number_of_axle=2
            elif 70<axle_ht1<130 and max_hgt>100 and gnd_clr_ON<40:
                txt = '3,CJV'
                message_box(txt)
                Number_of_axle=2
            else:
                txt = '10,OSV'
                message_box(txt)
    except UnboundLocalError:
        txt='0,Non Tollable'
        message_box(txt)
    windows_counter=0
    try:
        background_cut()
        image_to_base64(j, txt, Number_of_axle, max_hgt, first_two_axle_distance, tandum)
        tandum = 'False'
        tandum_axle_status=0
    except UnboundLocalError:
        pass
    
'''################### Function is for showing the class in message box ######################'''
def message_box(txt):
    if len(txt)>5:
         message_font = font.Font(size=20)
    else:
        message_font = font.Font(size=28)
    mesg = Message(string_frame1, text= txt, font= message_font, justify = tk.CENTER, relief=RAISED, width = 180)  
    mesg.place(x=455, y=70, width=315, height=115, bordermode= OUTSIDE)
    mesg.config(bg='white')
    txt = 'No Vehicle!!'


newData_1 = []
def background_cut():
    BGC = open("/home/tollman/AVC/image.png","rb")
    root.img_3 = img_3 = PIL.Image.open(BGC).convert("L")
    img_5 = img_3.convert("RGBA")
    datas = img_5.getdata()
    for item in datas:
        if item[0] >= 250 and item[1] >= 250 and item[2] >= 250:
            newData_1.append((255, 255, 255, 0))
        else:
            newData_1.append(item)
    img_5.putdata(newData_1)
    ImageDraw.floodfill(img_5,xy=(0,0),value=(255,0,255),thresh=10)
    img_5.save("/home/tollman/AVC/image1.png","PNG", optimize = True)

    
''' ################### Function is converting image into base64 string
and also saving class in string format into the particular text file
and also updating the count values ######################'''    
def image_to_base64(j, txt, Number_of_axle, max_hgt, first_two_axle_distance, tandum):
    td1 = dt.datetime.now()   #saving class into text file
    td = td1.strftime("%d-%m-%Y")
    directory_path_main='/home/tollman/AVC/'
    directory_name_main='String_file'
    try:
        path = os.path.join(directory_path_main,directory_name_main)
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        pass
    concatenate_path = directory_path_main + directory_name_main
    directory_name = td
    try:
        path = os.path.join(concatenate_path,directory_name)
        new_file_path = os.path.join(path, str(j)+'.txt')
        new_file = open(new_file_path,'a')
        new_file.writelines(str(txt))
        new_file.close()
    except OSError as error:
        pass
    with open("/home/tollman/AVC/image1.png", 'rb') as fs:
        my_string = base64.b64encode(fs.read())
        my_string1 = my_string.decode('utf-8') #Updating the count values
        td1 = date.today()
        td = td1.strftime("%d-%m-%Y")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        with open('/home/tollman/AVC/count.txt', 'w') as f:
            f.write(str(j))
        gen_str=    "S," +str(j)+ "," +str(txt)+ "," +str(Number_of_axle)+ "," +str(max_hgt)+ ",0.00,0.00,0.00," +str(first_two_axle_distance)+ "," +str(tandum)+ ", False, F," +str(my_string1)+ "," +str(td)+ "," +str(current_time)+ ",E"
    send_data(gen_str)
    
''' ################### Mutli threading function ######################'''    
def send_data(gen_str):
    global connection
    try:
        thread1 = threading.Thread(target = broadcasting_function, args=(gen_str,), daemon = True)
        thread1.start()
        try:
            if not connection:
                thread2 = threading.Thread(target = client_server, daemon = True).start()
            else:
                pass
        except NameError:
            pass
    except OSError as error:
        pass
def client_server():
    global connection, clients, clients_lock,ob
    print("server is listening")
    while True:
        connection, addr = ob.accept()

thread3 = threading.Thread(target = client_server, daemon = True).start()

def broadcasting_function(gen_str):
    global connection, clients, clients_lock
    try:
        with clients_lock:
            clients.add(connection)
        conc = str(connection)
        if len(conc) > 140:
            try:
                while True:
                    if not gen_str:
                        break
                    else:
                        with clients_lock:
                            for connections in clients:
                                connections.sendall(str.encode(gen_str))
                            gen_str=""
            except ConnectionError:
                if connection in clients:
                    clients.remove(connection)
                return
        else:
            if connection in clients:
                clients.remove(connection)
            connection=""
            return
    except NameError:
        pass
    

''' ################### While loop for GUI ######################'''
while True:
    try:
        root.update()
        checkSerialPort()
        datacanvas.config(scrollregion = datacanvas.bbox("all"))
    except TclError:
        root.mainloop()
        break  
root.mainloop()
