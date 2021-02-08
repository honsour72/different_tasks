import numpy as np

def orientation_2():
    global q
    f2 = open('catalog_coords.txt','r')
    v = dict()

    for line in f2:
        s = line.split()
        v[int(s[0])]=np.array([float(s[1]), float(s[2]), float(s[3])])
    f2.close()



    def get_dcm(v1, v2):
        vx = v1 / np.linalg.norm(v1)
        tmp = np.cross(v1,v2)
        vy = tmp / np.linalg.norm(tmp)
        vz = np.cross(vx, vy)
        a = np.array([vx, vy, vz]).T
        return a

    f = open('detected_triangles.txt','r')
    for line in f:
        s = line.split()
        s1 = v[int(s[0])]
        s2 = v[int(s[1])]
        t1 = np.array([float(s[2]), float(s[3]), float(s[4])])
        t2 = np.array([float(s[5]), float(s[6]), float(s[7])])
        q1 = get_dcm(s1, s2)
        q2 = get_dcm(t1, t2)
        q = q2 @ q1.T

        # print(q)
    f.close()
    return q





