# Indoor Navigation Prototype — all seven methodology steps

This project integrates camera capture, object detection, visual landmark localization, a predefined map, weighted graph routing, shortest-path planning, and step-by-step directions with obstacle alerts.

## Local run

Backend: Python 3.11 is recommended. Install the dependencies and launch the service:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

The first YOLO run downloads the pretrained `yolov8n.pt` weights. Set `YOLO_MODEL` to a compatible local `.pt` file to use custom trained weights. Frontend (second terminal):

```powershell
cd web
npm install
npm run dev
```

Open http://localhost:5173. To navigate from a source image, first add reference landmark photos as described below, then upload a photo of one of those locations and select a destination. The app matches the source photo, detects objects, plans a route, and displays distance-aware direction steps. Camera access requires localhost or HTTPS and browser permission. Phone browsers can use the image capture fallback.

## Deploy

The root `Dockerfile` builds the React frontend and runs it with the FastAPI backend as a single service. `render.yaml` is a Render Blueprint configuration. Push this folder to a Git repository, create a Render Blueprint from that repository, and deploy the `indoor-navigation` service. The app listens on port 8000 and checks health at `/api/health`. The first startup downloads YOLOv8 nano weights; larger/custom weights need adequate disk and memory. A deployment account and Git repository connection are needed to publish a public URL.

## Add a building map and landmark references

- Edit `backend/map_data.py` with the actual locations, measured walkway distances, and edges.
- Add reference photos under `backend/landmarks/` named by node ID (`entrance.jpg`, `openspace.jpg`, etc.). Provide clear, varied viewpoints; current ORB/RANSAC matcher selects the candidate with the most geometric inliers.
- Set `YOLO_MODEL` to a compatible custom model if you have one. Without it the app uses the pretrained general YOLOv8 nano model and recognizes only its classes. Object classes supplied to route planning can close matching edges as configured in `map_data.py`.

This remains a prototype. Example map coordinates and distances are illustrative, and vision accuracy depends on the supplied photos, camera conditions, and model. Do not use as the sole means of safety-critical navigation.
