from pathlib import Path
import cv2
import numpy as np
from map_data import NODES

REF_DIR=Path(__file__).parent/'landmarks'

def locate(frame):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    orb=cv2.ORB_create(nfeatures=2500)
    qkp,qdes=orb.detectAndCompute(gray,None)
    if qdes is None: return None
    matcher=cv2.BFMatcher(cv2.NORM_HAMMING)
    ranked=[]
    for node in NODES:
        path=next((p for p in (REF_DIR/f'{node}.jpg',REF_DIR/f'{node}.jpeg',REF_DIR/f'{node}.png') if p.exists()),None)
        if path is None: continue
        ref=cv2.imread(str(path),cv2.IMREAD_GRAYSCALE)
        if ref is None: continue
        rkp,rdes=orb.detectAndCompute(ref,None)
        if rdes is None or len(rkp)<4: continue
        pairs=matcher.knnMatch(qdes,rdes,k=2)
        good=[a for a,b in pairs if a.distance<0.72*b.distance]
        inliers=0
        if len(good)>=4:
            src=np.float32([qkp[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst=np.float32([rkp[m.trainIdx].pt for m in good]).reshape(-1,1,2)
            _,mask=cv2.findHomography(src,dst,cv2.RANSAC,5.0)
            inliers=int(mask.sum()) if mask is not None else 0
        ranked.append((inliers,len(good),node))
    if not ranked: return None
    ranked.sort(reverse=True)
    ins,good,node=ranked[0]
    if ins<8: return None
    return {'node':node,'name':NODES[node]['name'],'inliers':ins,'matches':good,'confidence':round(min(0.99,ins/max(good,1)),2),'method':'ORB + RANSAC'}
