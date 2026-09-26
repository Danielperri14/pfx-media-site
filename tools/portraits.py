#!/usr/bin/env python3
"""Build the team portraits for the PFX Media site from the white-background studio shots.
Cuts out the white (border-connected flood fill), decontaminates the white fringe on hair
(band around the matte edge + enclosed white gaps between curls, only where the surroundings
are dark hair so eyes/skin are never touched), crops square head-and-shoulders, and sets each
on the site's dark cyan->purple glow with a fade into the card colour.
Usage: python3 tools/portraits.py   (writes assets/daniel.jpg and assets/felix.jpg)"""
from PIL import Image, ImageFilter
import numpy as np, os
from collections import deque
D='/Volumes/PortableSSD/PB ALL Assets/PFP: Photos/Photos/'
SRC={'daniel':D+'Daniel Perri - High Res-7.jpg','felix':D+'ChatGPT Image Sep 27, 2026, 04_07_38 AM.png'}
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets')
PANEL=(16,16,22)
def matte(im, tol=28):
    a=np.asarray(im.convert('RGB')).astype(int); H,W,_=a.shape
    near=(a.min(axis=2)>255-tol); bg=np.zeros((H,W),bool); q=deque()
    for x in range(W):
        for y in (0,H-1):
            if near[y,x] and not bg[y,x]: bg[y,x]=True; q.append((y,x))
    for y in range(H):
        for x in (0,W-1):
            if near[y,x] and not bg[y,x]: bg[y,x]=True; q.append((y,x))
    while q:
        y,x=q.popleft()
        for ny,nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if 0<=ny<H and 0<=nx<W and near[ny,nx] and not bg[ny,nx]: bg[ny,nx]=True; q.append((ny,nx))
    return ~bg
def cutout(im, band_px, chroma_max):
    rgb=np.asarray(im.convert('RGB')).astype(float); fg=matte(im)
    A=Image.fromarray((fg*255).astype(np.uint8)); k=band_px*2+1
    band=(np.asarray(A.filter(ImageFilter.MaxFilter(k)))>0)&(np.asarray(A.filter(ImageFilter.MinFilter(k)))<255)
    mx=rgb.max(axis=2); mn=rgb.min(axis=2); grey=(mx-mn)<chroma_max      # skin is chromatic -> never "grey"
    local=np.asarray(Image.fromarray(rgb.mean(axis=2).astype(np.uint8)).filter(ImageFilter.BoxBlur(12))).astype(float)
    edge_fix=band&grey&fg                                                # white fringe along the matte edge
    pocket=fg&grey&(mx>185)&(local<80)                                   # white gaps between curls, only inside dark hair
    fix=edge_fix|pocket
    a_est=np.clip((255-mx)/(255-60),0,1)                                 # C = a*F + (1-a)*255  ->  a from brightness
    alpha=np.where(fix,np.minimum(fg.astype(float),a_est),fg.astype(float))
    a_safe=np.clip(alpha,0.05,1)[...,None]
    F=np.clip((rgb-(1-a_safe)*255)/a_safe,0,255)                        # ...and the true foreground colour solved back
    out=np.where(fix[...,None],F,rgb)
    a_img=Image.fromarray((alpha*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.9))
    res=Image.fromarray(out.astype(np.uint8)).convert('RGBA'); res.putalpha(a_img); return res
def compose(name, fx, fy, fw, band_px, chroma_max, size=900):
    im=Image.open(SRC[name]); W,H=im.size
    if W>1600: im=im.resize((1600,int(H*1600/W)),Image.LANCZOS); W,H=im.size
    side=int(fw*W); x0=int(fx*W-side/2); y0=int(fy*H)
    cut=cutout(im,band_px,chroma_max).crop((x0,y0,x0+side,y0+side)).resize((size,size),Image.LANCZOS)
    yy,xx=np.mgrid[0:size,0:size]; g=np.full((size,size,3),PANEL,float)
    def rad(cx,cy,r,col,kk):
        w=np.clip(1-np.sqrt((xx-cx)**2+(yy-cy)**2)/r,0,1)**2*kk
        for i,c in enumerate(col): g[:,:,i]+=w*c
    rad(size*0.2,size*0.25,size*0.9,(111,231,255),0.22); rad(size*0.95,size*0.35,size*0.8,(138,92,246),0.35)
    canvas=Image.fromarray(np.clip(g,0,255).astype(np.uint8)).convert('RGBA'); canvas.alpha_composite(cut)
    fd=np.zeros((size,size,4),np.uint8); fd[:,:,:3]=PANEL; fd[:,:,3]=(np.clip((yy-size*0.74)/(size*0.26),0,1)**1.6*255).astype(np.uint8)
    canvas.alpha_composite(Image.fromarray(fd))
    canvas.convert('RGB').save(os.path.join(OUT,f'{name}.jpg'),quality=88,optimize=True); print(name,'ok')
if __name__=='__main__':
    compose('daniel',0.50,0.01,0.52,10,40)
    compose('felix', 0.48,0.02,0.74,14,44)
