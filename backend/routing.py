import heapq
from map_data import NODES, EDGES

def shortest_path(start, goal, blocked_labels=frozenset()):
    graph={n:[] for n in NODES}
    for e in EDGES:
        if blocked_labels.intersection(e.get("obstacle_classes",[])): continue
        a,b=e["from"],e["to"]; w=float(e["distance"])
        graph[a].append((b,w)); graph[b].append((a,w))
    queue=[(0.0,start,[])]; best={}
    while queue:
        cost,node,path=heapq.heappop(queue)
        if node in best and best[node]<=cost: continue
        best[node]=cost; path=path+[node]
        if node==goal: return path,cost
        for neighbor,weight in graph[node]:
            if neighbor not in best: heapq.heappush(queue,(cost+weight,neighbor,path))
    return [],float("inf")

def _heading(a, b):
    dx=NODES[b]["x"]-NODES[a]["x"]
    dy=NODES[b]["y"]-NODES[a]["y"]
    labels=["east","southeast","south","southwest","west","northwest","north","northeast"]
    import math
    return labels[round(math.degrees(math.atan2(dy,dx))/45)%8]

def directions_for(path, blocked_labels=frozenset()):
    result=[]
    for i,node in enumerate(path):
        name=NODES[node]["name"]
        if len(path)==1:
            text=f"You are already at {name}."
        elif i==0:
            nxt=path[i+1]
            dist=next(float(e["distance"]) for e in EDGES if {e["from"],e["to"]}=={node,nxt})
            text=f"Start at {name}. Head {_heading(node,nxt)} toward {NODES[nxt]['name']} for {dist:g} m."
        elif i==len(path)-1:
            text=f"Arrive at {name}; your destination is here."
        else:
            prev,nxt=path[i-1],path[i+1]
            before=(NODES[node]["x"]-NODES[prev]["x"],NODES[node]["y"]-NODES[prev]["y"])
            after=(NODES[nxt]["x"]-NODES[node]["x"],NODES[nxt]["y"]-NODES[node]["y"])
            cross=before[0]*after[1]-before[1]*after[0]
            dot=before[0]*after[0]+before[1]*after[1]
            import math
            angle=abs(math.degrees(math.atan2(cross,dot)))
            turn="Continue straight"
            if angle>=30: turn="Turn right" if cross>0 else "Turn left"
            dist=next(float(e["distance"]) for e in EDGES if {e["from"],e["to"]}=={node,nxt})
            text=f"At {name}, {turn.lower()} and head {_heading(node,nxt)} toward {NODES[nxt]['name']} for {dist:g} m."
        result.append({"step":i+1,"node":node,"text":text})
    alerts=set()
    for edge in EDGES:
        alerts.update(blocked_labels.intersection(edge.get("obstacle_classes",[])))
    if alerts:
        result.insert(-1 if len(result)>1 else 0,{"step":None,"alert":True,"text":f"Obstacle alert: detected {', '.join(sorted(alerts))}. Routes near affected walkways were avoided where possible."})
    return result
