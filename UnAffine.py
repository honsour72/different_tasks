from PIL import Image, ImageFilter
import math
import numpy as np


im = Image.open('correction left.jpg')
 
threshold=50

lut = [0]*threshold+[255]*(256-threshold)

im2 = im.convert('L')
im4 = im2.point(lut)
##im4.show()



def FindStars(ima):
    pix = ima.load()
    
    def GetStar(i, j):
        nonlocal npoint, xs, ys
        if i<0 or i>=ima.width or j<0 or j>=ima.height or pix[i,j] != 255: return None    
        npoint += 1
        xs += i
        ys += j
        pix[i,j] = 200
        GetStar(i, j+1)
        GetStar(i+1, j)
        GetStar(i-1, j)
        GetStar(i, j-1)    

    stars = []
    for i in range(ima.width):
        for j in range(ima.height):
            if pix[i,j] == 255:
                xs, ys = 0, 0
                npoint = 0
                GetStar(i,j)
                xs /= npoint
                ys /= npoint
                stars.append((xs, ys, npoint))
    print (stars)            
    return stars


stars = FindStars(im4)

ss = sorted(stars, key=lambda star: star[1])
SortedStars = sorted(ss[0:3], key=lambda star: star[0]) +\
     sorted(ss[3:6], key=lambda star: star[0]) +\
     sorted(ss[6:9], key=lambda star: star[0])

##print(SortedStars)


FP = 512
refStars = []
for i in range(-1, 2):
    for j in range (-1, 2):
        refStars.append((FP * j / 3 +FP / 2, FP* i / 3 + FP / 2))

##print(refStars)

def GetAffine(s, t):
    xm = np.zeros((len(t),3))
    ymx = np.zeros((len(t),1))
    ymy = np.zeros((len(t),1))
    ax = np.zeros((3,1))
    ay = np.zeros((3,1))
    a = np.zeros((3,3))
    
    
    for i in range(len(t)):
        xm[i,2] = 1
        xm[i,0] = s[i][0]
        xm[i,1] = s[i][1]
        ymx[i,0] = t[i][0]
        ymy[i,0] = t[i][1]
    
    ax = (np.linalg.inv(xm.T @ xm))@(xm.T @ ymx)    
    ay = (np.linalg.inv(xm.T @ xm))@(xm.T @ ymy)

    a[0] = ax[:,0]
    a[1] = ay[:,0]
    a[2,2] = 1

    a = np.linalg.inv(a)
    
    return a[0,0], a[0,1], a[0,2], a[1,0], a[1,1], a[1,2]
        
        

    
a, b, c, d, e, f = GetAffine(SortedStars, refStars)       
print(a, b, c)
print(d, e, f)
# im4.show()
cim = im4.transform((FP,FP), Image.AFFINE, (a,b,c,d,e,f), resample=Image.BICUBIC)
cim = cim.point(lut)
# cim.show()


im = Image.open('orientation left.jpg')
#im = Image.open('dots_1.bmp')

im2 = im.convert('L')
cim = im2.transform((FP,FP), Image.AFFINE, (a,b,c,d,e,f), resample=Image.BICUBIC)
cim = cim.point(lut)
cim.save("detected_stars_foto.jpg")
# cim.show()
st = FindStars(cim)

f2 = open('detected_stars.txt', 'w')
print(len(st), file = f2)
for s in st:
    print(s[0],s[1], file = f2)
f2.close()
