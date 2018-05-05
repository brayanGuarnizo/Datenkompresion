from PIL import Image
import numpy as np
import scipy.fftpack
import tkinter as tk
import huffman4 as hu
from matplotlib import pyplot as plt 

#http://www-lehre.inf.uos.de/nwa/mm/vortrag/node31.html



#input is a RGB numpy array with shape (height,width,3), can be uint,int, float or double, values expected in the range 0..255
#output is a double YUV numpy array with shape (height,width,3), values in the range 0..255
def RGB2YUV( rgb ):
     
    m = np.array([[ 0.29900, -0.16874,  0.50000],
                 [0.58700, -0.33126, -0.41869],
                 [ 0.11400, 0.50000, -0.08131]])
     
    yuv = np.dot(rgb,m)
    yuv[:,:,1:]+=128.0
    return yuv

#input is an YUV numpy array with shape (height,width,3) can be uint,int, float or double,  values expected in the range 0..255
#output is a double RGB numpy array with shape (height,width,3), values in the range 0..255
def YUV2RGB( yuv ):
      
    m = np.array([[ 1.0, 1.0, 1.0],
                 [-0.000007154783816076815, -0.3441331386566162, 1.7720025777816772],
                 [ 1.4019975662231445, -0.7141380310058594 , 0.00001542569043522235] ])
    
    rgb = np.dot(yuv,m)
    rgb[:,:,0]-=179.45477266423404
    rgb[:,:,1]+=135.45870971679688
    rgb[:,:,2]-=226.8183044444304
    return rgb



def rounding(array01):
    array02=[[]]
    for i in range(0,len(array01)):
        temparray02=[]
        for k in range(0,8):
            r=str(array01[i][k])
            j=0
          
            while(r[j]!="."):
                j=j+1
            r=r[:j]
          
            temparray02.append(int(r))
        if i==0:
            array02=temparray02
        else:
            array02=np.vstack((array02, temparray02))
        
    return array02        



def quantisierung(imagematrix, select):
    m1=np.array([[16,11,10,16,24,40,51,61],
                [12,12,14,19,26,58,60,55],
                [14,13,16,24,40,57,69,56],
                [14,17,22,29,51,87,80,62],
                [18,22,37,56,68,109,103,77],
                [24,35,55,64,81,104,113,92],
                [49,64,78,87,103,121,120,101],
                [72,72,95,98,112,100,103,99]])
    
    m2=np.array([[17,18,24,47,99,99,99,99],
                [18,21,26,66,99,99,99,99],
                [24,26,56,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99]])
    
    m3=np.array([[3,5,7,9,11,13,15,17],
                [5,7,9,11,13,15,17,19],
                [7,9,11,13,15,17,19,21],
                [9,11,13,15,17,19,21,23],
                [11,13,15,17,19,21,23,25],
                [13,15,17,19,21,23,25,27],
                [15,17,19,21,23,25,27,29],
                [17,19,21,23,25,27,29,31]])
    m4=np.array([[1,3,5,7,9,11,13,15],
                [3,5,7,9,11,13,15,17],
                [5,7,9,11,13,15,17,19],
                [7,9,11,13,15,17,19,21],
                [9,11,13,15,17,19,21,23],
                [11,13,15,17,19,21,23,25],
                [13,15,17,19,21,23,25,27],
                [15,17,19,21,23,25,27,29]])
    
    m5=np.array([[1,1,1,3,5,7,9,11],
                [1,1,3,5,7,9,11,13],
                [1,3,5,7,9,11,13,15],
                [3,5,7,9,11,13,15,17],
                [5,7,9,11,13,15,17,19],
                [7,9,11,13,15,17,19,21],
                [9,11,13,15,17,19,21,23],
                [11,13,15,17,19,21,23,25]])
    
    if (select==1):
        m=m1
    elif (select==2):
        m=m2
    elif(select==3):
        m=m3
    elif(select==4):
        m=m4
    else:
        m=m5
    NewLena=open("NewLena.txt","w")
    NewLena.write(str(select)+"\n")
    result=[[]]
    temparray02=[[]]
    
   
    imagearray=np.array(imagematrix)
   
    for i in range(0,len(imagearray),8):
    
        
        for j in range(0,len(imagearray[0]),8):
            temparray01=(imagearray[i:i+8,j:j+8]/m)
           
            temparray01=rounding(temparray01)
           
            if (j==0) :
                temparray02=temparray01
            elif (j>0):
                temparray02=np.hstack((temparray02, temparray01))
            
        if(i==8):
            result=temparray02
        elif(i>8):
          
            result=np.vstack((result,temparray02))   
                
                
  
    
    result=np.vstack((result,temparray02))
 
    
    return result

def requantisierung(imagematrix, select):
    m1=np.array([[16,11,10,16,24,40,51,61],
                [12,12,14,19,26,58,60,55],
                [14,13,16,24,40,57,69,56],
                [14,17,22,29,51,87,80,62],
                [18,22,37,56,68,109,103,77],
                [24,35,55,64,81,104,113,92],
                [49,64,78,87,103,121,120,101],
                [72,72,95,98,112,100,103,99]])
    
    m2=np.array([[17,18,24,47,99,99,99,99],
                [18,21,26,66,99,99,99,99],
                [24,26,56,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99]])
    
    m3=np.array([[3,5,7,9,11,13,15,17],
                [5,7,9,11,13,15,17,19],
                [7,9,11,13,15,17,19,21],
                [9,11,13,15,17,19,21,23],
                [11,13,15,17,19,21,23,25],
                [13,15,17,19,21,23,25,27],
                [15,17,19,21,23,25,27,29],
                [17,19,21,23,25,27,29,31]])
    
    m4=np.array([[1,3,5,7,9,11,13,15],
                [3,5,7,9,11,13,15,17],
                [5,7,9,11,13,15,17,19],
                [7,9,11,13,15,17,19,21],
                [9,11,13,15,17,19,21,23],
                [11,13,15,17,19,21,23,25],
                [13,15,17,19,21,23,25,27],
                [15,17,19,21,23,25,27,29]])
    
    m5=np.array([[1,1,1,3,5,7,9,11],
                [1,1,3,5,7,9,11,13],
                [1,3,5,7,9,11,13,15],
                [3,5,7,9,11,13,15,17],
                [5,7,9,11,13,15,17,19],
                [7,9,11,13,15,17,19,21],
                [9,11,13,15,17,19,21,23],
                [11,13,15,17,19,21,23,25]])
    
    if (select==1):
        m=m1
    elif (select==2):
        m=m2
    elif(select==3):
        m=m3
    elif(select==4):
        m=m4
    else:
        m=m5
    
   
    result=[[]]
    temparray02=[[]]
    
   
    imagearray=np.array(imagematrix)
   
    for i in range(0,len(imagearray),8):
    
        
        for j in range(0,len(imagearray[0]),8):
           
                    
            temparray01=(imagearray[i:i+8,j:j+8]*m)
            
            if (j==0) :
                temparray02=temparray01
                
            elif (j>0):
                temparray02=np.hstack((temparray02, temparray01))
            
        if(i==8):
            result=temparray02
        elif(i>8):
           
            result=np.vstack((result,temparray02))   
                
                
  
    
    result=np.vstack((result,temparray02))
 
   
    return result





def Matrix2Vector(matrix):
    
    result=[]
    for k in range(0,len(matrix),8):
    
        
        for l in range(0,len(matrix[k]),8):
            tempresult=[]
           
            tempresult.append(matrix[k,l])
            tempresult.append(matrix[k,l+1])
            tempresult.append(matrix[k+1,l])
            tempresult.append(matrix[k+2,l])
            tempresult.append(matrix[k+1,l+1])
            tempresult.append(matrix[k,l+2])
            tempresult.append(matrix[k,l+3])
            tempresult.append(matrix[k+1,l+2])
            tempresult.append(matrix[k+2,l+1])
            tempresult.append(matrix[k+3,l])
            tempresult.append(matrix[k+4,l])
            tempresult.append(matrix[k+3,l+1])
            tempresult.append(matrix[k+2,l+2])
            tempresult.append(matrix[k+1,l+3])
            tempresult.append(matrix[k,l+4])
            tempresult.append(matrix[k,l+5])
            tempresult.append(matrix[k+1,l+4])
            tempresult.append(matrix[k+2,l+3])
            tempresult.append(matrix[k+3,l+2])
            tempresult.append(matrix[k+4,l+1])
            tempresult.append(matrix[k+5,l])
            tempresult.append(matrix[k+6,l])
            tempresult.append(matrix[k+5,l+1])
            tempresult.append(matrix[k+4,l+2])
            tempresult.append(matrix[k+3,l+3])
            tempresult.append(matrix[k+2,l+4])
            tempresult.append(matrix[k+1,l+5])
            tempresult.append(matrix[k,l+6])
            tempresult.append(matrix[k,l+7])
            tempresult.append(matrix[k+1,l+6])
            tempresult.append(matrix[k+2,l+5])
            tempresult.append(matrix[k+3,l+4])
            tempresult.append(matrix[k+4,l+3])
            tempresult.append(matrix[k+5,l+2])
            tempresult.append(matrix[k+6,l+1])
            tempresult.append(matrix[k+7,l])
            tempresult.append(matrix[k+7,l+1])
            tempresult.append(matrix[k+6,l+2])
            tempresult.append(matrix[k+5,l+3])
            tempresult.append(matrix[k+4,l+4])
            tempresult.append(matrix[k+3,l+5])
            tempresult.append(matrix[k+2,l+6])
            tempresult.append(matrix[k+1,l+7])
            tempresult.append(matrix[k+2,l+7])
            tempresult.append(matrix[k+3,l+6])
            tempresult.append(matrix[k+4,l+5])
            tempresult.append(matrix[k+5,l+4])
            tempresult.append(matrix[k+6,l+3])
            tempresult.append(matrix[k+7,l+2])
            tempresult.append(matrix[k+7,l+3])
            tempresult.append(matrix[k+6,l+4])
            tempresult.append(matrix[k+5,l+5])
            tempresult.append(matrix[k+4,l+6])
            tempresult.append(matrix[k+3,l+7])
            tempresult.append(matrix[k+4,l+7])
            tempresult.append(matrix[k+5,l+6])
            tempresult.append(matrix[k+6,l+5])
            tempresult.append(matrix[k+7,l+4])
            tempresult.append(matrix[k+7,l+5])
            tempresult.append(matrix[k+6,l+6])
            tempresult.append(matrix[k+5,l+7])
            tempresult.append(matrix[k+6,l+7])
            tempresult.append(matrix[k+7,l+6])
            tempresult.append(matrix[k+7,l+7])
                    
            result.append(tempresult)
  
    return result



def Vector2Code(doublevector):
    
    result=[]
    for i in range(0,int(len(doublevector))):
        counter=0
        tempresult=[]
        for j in range(0,len(doublevector[i])):
           
            if j==0:
                tempresult.append((-1,doublevector[i][0]))
                
            elif doublevector[i][j]==0:
                counter=counter+1
          
            elif doublevector[i][j]!=0:
                tempresult.append((counter,doublevector[i][j]))
                counter=0
            if j==63:
                tempresult.append((0,0))
                counter=0
       
        result.append(tempresult)
    return result    



def counttuples(doublevector):
    counter=0
    for i in range(0,int(len(doublevector))):       
        for j in range(0,len(doublevector[i])):
            counter=counter+1
            
    return counter


def modify(tomodify,select):
    tempimage=np.zeros((len(tomodify),(len(tomodify[0])),3),int)
    for i in range(0,len(tomodify)):
        for j in range (0,len(tomodify[i])):
            for k in range(0,len(tomodify[i][j])):
               
                tempimage[i][j][k]=tomodify[i][j][k]+select
    return tempimage


def twodim2onedim(tomodify):
    result=[]
   
    for i in range(0,len(tomodify)):
        
        for j in range(0,len(tomodify[i])):
            result.append(tomodify[i][j])
   
    return result

def switchdict(tomodify):
    result={}
    for key in (tomodify.keys()):
        result.update({tomodify[key],key})
    return result


def createhuffman(xquanty):
    xvector=Matrix2Vector(xquanty)
    xcode=Vector2Code(xvector)
    xcodeflat=twodim2onedim(xcode)
    xcodefreq=hu.frequency(xcodeflat)
    xcodetuples=hu.sortFreq(xcodefreq)

    xtree=hu.buildTree(xcodetuples)

    xtrim=hu.trimTree(xtree)

    hu.assignCodes(xtrim)
    xencoded=hu.encode(xcodeflat)
   
    newLena=open("newLena.txt","a")
    newLena.write("Tree: "+str(xtrim)+"\n"+str(xencoded)+"\n")
    newLena.close()
    return xtrim,xencoded


def code2vector(jpgcode):
    result=[]
    for item in jpgcode:
     
        if(item[0]==-1):
            counter=0
            vector=[]
            
        if(item[1]!=0) or (item[0]==-1):
            if(item[0]==0 or item[0]==-1):
                vector.append(item[1])
                counter=counter+1
             
            elif(item[0]>0):
                for i in range(item[0]):
                    vector.append(0)
                    counter=counter+1
                vector.append(item[1])
                counter=counter+1
              
        else:   
            for j in range(0,64-counter):
                vector.append(0)
           
            if(len(vector))>64:
                print(vector)
            result.append(vector)
   
    return result
 

def vector2matrix(vector):
    
    result=[[]]
    tempresult02=[[]]
    for i in range(0,len(vector)):
      
        if(len(vector[i]))>64:
            print(vector[i])
            print(i)
       
        tempresult=np.zeros((8,8),int)
        k,l=0,0
        tempresult[0,0]=vector[i][0]
        tempresult[0,1]=vector[i][1]
        tempresult[1,0]=vector[i][2]
        tempresult[k+2,l]=vector[i][3]
        tempresult[k+1,l+1]=vector[i][4]
        tempresult[k,l+2]=vector[i][5]
        tempresult[k,l+3]=vector[i][6]
        tempresult[k+1,l+2]=vector[i][7]
        tempresult[k+2,l+1]=vector[i][8]
        tempresult[k+3,l]=vector[i][9]
        tempresult[k+4,l]=vector[i][10]
        tempresult[k+3,l+1]=vector[i][11]
        tempresult[k+2,l+2]=vector[i][12]
        tempresult[k+1,l+3]=vector[i][13]
        tempresult[k,l+4]=vector[i][14]
        tempresult[k,l+5]=vector[i][15]
        tempresult[k+1,l+4]=vector[i][16]
        tempresult[k+2,l+3]=vector[i][17]
        tempresult[k+3,l+2]=vector[i][18]
        tempresult[k+4,l+1]=vector[i][19]
        tempresult[k+5,l]=vector[i][20]
        tempresult[k+6,l]=vector[i][21]
        tempresult[k+5,l+1]=vector[i][21]
        tempresult[k+4,l+2]=vector[i][22]
        tempresult[k+3,l+3]=vector[i][23]
        tempresult[k+2,l+4]=vector[i][24]
        tempresult[k+1,l+5]=vector[i][25]
        tempresult[k,l+6]=vector[i][26]
        tempresult[k,l+7]=vector[i][27]
        tempresult[k+1,l+6]=vector[i][28]
        tempresult[k+2,l+5]=vector[i][29]
        tempresult[k+3,l+4]=vector[i][30]
        tempresult[k+4,l+3]=vector[i][31]
        tempresult[k+5,l+2]=vector[i][32]
        tempresult[k+6,l+1]=vector[i][33]
        tempresult[k+7,l]=vector[i][34]
        tempresult[k+7,l+1]=vector[i][35]
        tempresult[k+6,l+2]=vector[i][36]
        tempresult[k+5,l+3]=vector[i][37]
        tempresult[k+4,l+4]=vector[i][38]
        tempresult[k+3,l+5]=vector[i][39]
        tempresult[k+2,l+6]=vector[i][40]
        tempresult[k+1,l+7]=vector[i][41]
        tempresult[k+2,l+7]=vector[i][42]
        tempresult[k+3,l+6]=vector[i][43]
        tempresult[k+4,l+5]=vector[i][44]
        tempresult[k+5,l+4]=vector[i][45]
        tempresult[k+6,l+3]=vector[i][46]
        tempresult[k+7,l+2]=vector[i][47]
        tempresult[k+7,l+3]=vector[i][48]
        tempresult[k+6,l+4]=vector[i][49]
        tempresult[k+5,l+5]=vector[i][50]
        tempresult[k+4,l+6]=vector[i][51]
        tempresult[k+3,l+7]=vector[i][52]
        tempresult[k+4,l+7]=vector[i][53]
        tempresult[k+5,l+6]=vector[i][54]
        tempresult[k+6,l+5]=vector[i][55]
        tempresult[k+7,l+4]=vector[i][56]
        tempresult[k+7,l+5]=vector[i][57]
        tempresult[k+6,l+6]=vector[i][58]
        tempresult[k+5,l+7]=vector[i][59]
        tempresult[k+6,l+7]=vector[i][60]
        tempresult[k+7,l+6]=vector[i][61]
        tempresult[k+7,l+7]=vector[i][62]
        
        
        if(i%64 ==0) and (i==64):
           
            result=tempresult02
            #tempresult=np.zeros((8,8),int)
        elif(i%64==0) and (i>64):
            
            result=np.vstack((result,tempresult02))
            
            #tempresult=np.zeros((8,8),int)
        if(i%64==0):
            
            tempresult02=tempresult
            
        elif(i%64 != 0):
           tempresult02=np.hstack((tempresult02,tempresult))
   
    result=np.vstack((result,tempresult02))    
    
    return result          

def compress(file):
    img01=Image.open(file)
    #img1=img.convert('RGB')
    img_yuv=Image.fromarray(RGB2YUV(img01).astype(np.uint8))
    img_invert=modify(np.asanyarray(img_yuv),-128)
   # plt.hist(img_invert[1],bins=20,)
   # plt.show()
    dt_image=scipy.fftpack.dct(img_invert,2,axis=-1,norm='ortho', overwrite_x=False)
    #plt.hist(dt_image[1])
    #plt.show()
    y=dt_image[:,:,0]
    u=dt_image[:,:,1]
    #plt.hist(u,bins=20)
    #plt.show()
    v=dt_image[:,:,2]
    yquant=quantisierung(np.asanyarray(y),3)
    uquant=quantisierung(np.asanyarray(u),3)
    vquant=quantisierung(np.asanyarray(v),3)
    #plt.hist(uquant,bins=20)
    #plt.show()
   
    #plt.hist(uquant,bins=10)
    #plt.show()
    ytree,yencoded=createhuffman(yquant)
    utree,uencoded=createhuffman(uquant)
    vtree,vencoded=createhuffman(vquant)
   # plt.hist(uencoded,bins=2)
    ydecoded=hu.decode(ytree,yencoded)
    udecoded=hu.decode(utree,uencoded)
    vdecoded=hu.decode(vtree,vencoded)
    #print(ydecoded)
    yvector=code2vector(ydecoded)
    uvector=code2vector(udecoded)
    vvector=code2vector(vdecoded)
    
    yquant02=vector2matrix(yvector)
    uquant02=vector2matrix(uvector)
    vquant02=vector2matrix(vvector)
    reyqant=requantisierung(np.asanyarray(yquant02),3)
    reuqant=requantisierung(np.asanyarray(uquant02),3)
    revqant=requantisierung(np.asanyarray(vquant02),3)

    new_image=np.dstack((reyqant,reuqant,revqant))
    new_dt=scipy.fftpack.idct(new_image,2,axis=-1,norm='ortho', overwrite_x=False)

    dummy=modify(new_dt,128)
    dummy2=YUV2RGB(dummy).astype(np.uint8)
    new_rgbimage=Image.fromarray(dummy2)
    #new_rgbimage.show()
    
    new_rgbimage.save("compressedLena.png")
    return new_rgbimage
    
    


#compress("Lenna.png")


    
    
def button_compress():
    #imglab.destroy()
    imglab.config(image="",text="Here as an Example the three RGB colourlayers.\n Every Pixels has three values between 0 and 255.\nWhat the JPG conversion is doing next, it convert the RGB layout to the YCrCB layout.\n Click it to see how that looks like.",font=('Arial',15))
    #imglab.config(text="Hier als Beispiel die drei Farblayer",font=('Arial',20))
    textlab01.config(image=img01)
    textlab02.config(image=img02)
    textlab03.config(image=img03)
    
def YCbCr():
    imglab.config(image="",text="Here as an Example the three YCbCr colourlayers.\n It is just a simple matrix multiplication:\nY = 0,299R + 0,587G + 0,114B\nCb = -0,1687R - 0,3313G + 0,5B + 128\nCr = 0,5R - 0,4187G - 0,0813B + 128",font=('Arial',15))
    textlab01.config(image=yimg01)
    textlab02.config(image=uimg02)
    textlab03.config(image=vimg03)
    
    
def YCbCrexpl():
    textlab01.config(image="",text="Sometimes here the compression begins\n by saving only an  average for the\n Cb and Cr layer.\nSo in RGB you need for four pixels\n with three values each twelve Bytes.\n For a subsamling like 4:2:2 you just need 8 Bytes.\n For a 4:1:1 subsampling (like to the right\n) you just need 6 Bytes.",font=('Arial',15))
    textlab02.config(image=eximageYCbCr)
    textlab03.config(image="",text="This works, because the\n human eye can not visualize these small differences.\n We do not use these subsampling\n in our example.\n Next comes the Indexshift.\n",font=('Arial',15))
    
def Indexshift():
    imglab.config(image=distribution01,text="")
    textlab01.config(image="",text="The historgramm above shows the distribution of the colourpixels from \n the y layer before the shift.\n The JPG conversion just does a -128 to every value.\n",font=('Arial',15))
    textlab02.config(image=distribution02,text="")
    textlab03.config(image="",text="The histogramm to the left shows the distribution after the shift.\n Now the values are centered around zero.\n That will be important for the next step.\n",font=('Arial',15))
        


testfile="Lenna.png"
root=tk.Tk()
root.geometry("800x800")
root.title("JPEG compression short explained")

framebutton=tk.Frame(root)
frameimg1=tk.Frame(root)

img1=tk.PhotoImage(file="D:/Uni/ss18/dk/Lenna.png")
imglab=tk.Label(frameimg1,image=img1)
img3=tk.PhotoImage(file="D:/Uni/ss18/dk/compressedLena.png")

frametext01=tk.Frame(root)

#RGB example and explanation
Lennaorginal=Image.open(testfile)
img1split,img2split,img3split=Lennaorginal.split()

img1split.save("LennaR.png")
img2split.save("LennaG.png")
img3split.save("LennaB.png")
img01=tk.PhotoImage(file="D:/Uni/ss18/dk/LennaR.png")
img02=tk.PhotoImage(file="D:/Uni/ss18/dk/LennaG.png")
img03=tk.PhotoImage(file="D:/Uni/ss18/dk/LennaB.png")

#YCbCr example and explanation
img_yuv=Image.fromarray(RGB2YUV(Lennaorginal).astype(np.uint8))
y,u,v=img_yuv.split()
y.save("LennaY.png")
u.save("LennaU.png")
v.save("LennaV.png")
yimg01=tk.PhotoImage(file="D:/Uni/ss18/dk/LennaY.png")
uimg02=tk.PhotoImage(file="D:/Uni/ss18/dk/LennaU.png")
vimg03=tk.PhotoImage(file="D:/Uni/ss18/dk/LennaV.png")
eximageYCbCr=tk.PhotoImage(file="D:/Uni/ss18/dk/15-yuv.gif")

#indexshift historgramms and explanation
img_invert=modify(np.asanyarray(img_yuv),-128)


plt.hist(img1split)
plt.title('Distribution of colourpixels bevor the shift')
plt.xlabel('Values of Pixel')
plt.ylabel('Number of Pixels')
plt.savefig("exam02.png")
plt.show()
plt.hist(img_invert[0],histtype='bar')

plt.title('Distribution of colourpixels after the shift')
plt.xlabel('Values of Pixel')
plt.ylabel('Number of Pixels')
plt.savefig("exam01.png")
plt.show()
distribution01=tk.PhotoImage(file="D:/Uni/ss18/dk/exam02.png")
distribution02=tk.PhotoImage(file="D:/Uni/ss18/dk/exam01.png")



#here starts the gui building
textlab01=tk.Label(frametext01,text="\n\nThat is our Example Picture. It is kind of famous. The size is 512*512*3, because it is saved as an RGB Image.\n That means 786432 Bytes allone for the values of the color.\n\n Click on Start to show the 3 Layers.",font=('Arial',15))
textlab02=tk.Label(frametext01)
textlab03=tk.Label(frametext01) 


Startbutton=tk.Button(framebutton,text="Start",font=('Arial',10),height=5,width=15,command=button_compress)
YCbCrbutton=tk.Button(framebutton,text="YCbCr convert",font=('Arial',10),height=5,width=15, command=YCbCr)
YCbCrbuttonexplanation=tk.Button(framebutton,text="YCbCr explanation",font=('Arial',10),height=5,width=15, command=YCbCrexpl)
Indexshiftbutton=tk.Button(framebutton,text="Indexshift",font=('Arial',10),height=5,width=15,command=Indexshift)

Exit_button=tk.Button(framebutton, text="Beenden",font=('Arial',10),height=5,width=15, command=root.destroy)


frameimg1.grid(row=0,column=0,sticky="w")
frametext01.grid(row=1,column=0)

framebutton.grid(row=0,column=1,sticky="e")
textlab01.grid(row=1,column=0,columnspan=1)
textlab02.grid(row=1,column=1,columnspan=1)
textlab03.grid(row=1,column=2,columnspan=1)
imglab.grid(row=0,column=0)
#anweisungs_label.grid(row=0,column=0,sticky="n")
Startbutton.grid(row=0,column=2, sticky="e")
YCbCrbutton.grid(row=1,column=2,sticky="e")
YCbCrbuttonexplanation.grid(row=2,column=2,sticky="e")
Indexshiftbutton.grid(row=3,column=2,sticky="e")


Exit_button.grid(row=5,column=2,sticky="e")

#info_label.pack()
#exit_button.pack()

root.mainloop()






