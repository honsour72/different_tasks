import numpy as np
f = open('detected_stars.txt', 'r')
n = int(f.readline())
w = 7
FP = 512
k = 1/np.tan(np.radians(w/2))

visible_stars = []
for i in range(n):
    y, z = [float(p) for p in f.readline().split()]
    yz = 2*(y - FP/2)/FP
    zz = -2*(z - FP/2)/FP
    
    q = np.array([k,yz,zz])
    q = q / np.linalg.norm(q)
    # print(yz, zz, q)
    visible_stars.append(q)
f.close()

dt_1 = np.dtype([('s0','i'),('s1','i'),('s2','i'),('r','d'),('l01','d'),('l02','d'),('l12','d')])
delone = np.loadtxt('catalog_del.txt', dtype=dt_1)
v = set()
eps = 0.01

fo = open('detected_triangles.txt', 'w')

def ChkStars(stCoords0, stCoords1, stCoords2):
    alpha0 = np.degrees(np.arccos(np.dot(stCoords0, stCoords1)))
    alpha1 = np.degrees(np.arccos(np.dot(stCoords0, stCoords2)))
    alpha2 = np.degrees(np.arccos(np.dot(stCoords1, stCoords2)))

    p = (alpha0 + alpha1 + alpha2) / 2
    sq = (p*(p-alpha0)*(p-alpha1)*(p-alpha2))**(1/2)
    r = alpha0 * alpha1 * alpha2 / (4 * sq)

    #print(r, alpha0, alpha1, alpha2)
    test = [424, 1107, 2609, 6789, 6811, 8546, 8938]

    for i in range(len(delone)):
        triangle = delone[i]
        #if (triangle[0] in test) and (triangle[1] in test) and (triangle[2] in test):
        if abs(r-triangle[6])<eps and abs(alpha0-triangle[3])<eps and abs(alpha1-triangle[4])<eps and abs(alpha2-triangle[5])<eps:
                    print(triangle[0], triangle[1], triangle[2], stCoords0, stCoords1, stCoords2)
                    v.add(i)
                    print(triangle[0], triangle[1], *stCoords0, *stCoords1, file=fo)
                    

    
for i0 in range(len(visible_stars)-2):
    for i1 in range(i0+1,len(visible_stars)-1):
        for i2 in range(i1+1,len(visible_stars)):
            ChkStars(visible_stars[i0], visible_stars[i1], visible_stars[i2])
            ChkStars(visible_stars[i0], visible_stars[i2], visible_stars[i1])
            ChkStars(visible_stars[i1], visible_stars[i0], visible_stars[i2])
            ChkStars(visible_stars[i1], visible_stars[i2], visible_stars[i0])
            ChkStars(visible_stars[i2], visible_stars[i0], visible_stars[i1])
            ChkStars(visible_stars[i2], visible_stars[i1], visible_stars[i0])
        
fo.close()
