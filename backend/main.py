from __future__ import annotations
import cv2, numpy as np
from pathlib import Path
from fastapi.responses import FileResponse
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from map_data import NODES, EDGES
from routing import shortest_path, directions_for
from localization import locate
from detection import detector

app=FastAPI(title="Indoor Navigation API",version="2.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
class RouteRequest(BaseModel):
 start:str; destination:str; detected_objects:list[str]=[]

def decode_upload(raw):
 arr=np.frombuffer(raw,np.uint8); frame=cv2.imdecode(arr,cv2.IMREAD_COLOR)
 if frame is None: raise HTTPException(400,"Could not read image frame")
 return frame
@app.get("/api/health")
def health(): return {"status":"ok","yolo_ready":detector.model is not None}
@app.get("/api/map")
def get_map(): return {"nodes":list(NODES.values()),"edges":EDGES}
@app.post("/api/analyze")
async def analyze(image:UploadFile=File(...)):
 frame=decode_upload(await image.read()); location=locate(frame); objects,error=detector.detect(frame)
 return {"location":location,"objects":objects,"detector_error":error,"route_obstacles":sorted({o['label'] for o in objects if o['label'] in {'chair','table','person','suitcase','bicycle','bench'}})}
@app.post("/api/localize")
async def localize_endpoint(image:UploadFile=File(...)):
 result=locate(decode_upload(await image.read()))
 if not result: raise HTTPException(422,"No reliable landmark match. Add reference photos named <node-id>.jpg under backend/landmarks/ and try again.")
 return result
@app.post("/api/route")
def route(req:RouteRequest):
 if req.start not in NODES or req.destination not in NODES: raise HTTPException(404,"Unknown start or destination")
 blocked={x.strip().lower() for x in req.detected_objects}
 path,distance=shortest_path(req.start,req.destination,blocked)
 if not path: raise HTTPException(422,"No available route. Try another destination or clear reported obstacles.")
 return {"path":path,"distance_m":round(distance,1),"directions":directions_for(path,blocked),"obstacles":[f"{x} detected; affected walkway edges were avoided where possible." for x in sorted(blocked & {'person','chair','table','suitcase','bicycle','bench'})]}

WEB_DIST=Path(__file__).resolve().parents[1]/"web"/"dist"
@app.get("/{asset_path:path}")
def frontend(asset_path:str):
 candidate=(WEB_DIST/asset_path).resolve()
 if WEB_DIST.exists() and candidate.is_relative_to(WEB_DIST) and candidate.is_file(): return FileResponse(candidate)
 if WEB_DIST.exists(): return FileResponse(WEB_DIST/"index.html")
 raise HTTPException(404,"Frontend build not found")
