# Coordinates are normalized to a 100 x 100 map canvas; distances are illustrative metres.
NODES={
 "entrance":{"id":"entrance","name":"Main Entrance","x":10,"y":52,"type":"entrance"},
 "junction":{"id":"junction","name":"Central Junction","x":38,"y":52,"type":"junction"},
 "openspace":{"id":"openspace","name":"Open Space","x":67,"y":24,"type":"landmark"},
 "studyarea":{"id":"studyarea","name":"Study Area","x":67,"y":78,"type":"landmark"},
 "meetingroom":{"id":"meetingroom","name":"Meeting Room","x":90,"y":52,"type":"room"},
}
# obstacle_classes make an edge unavailable if any matching detected class is reported.
EDGES=[
 {"from":"entrance","to":"junction","distance":12,"obstacle_classes":["chair","table"]},
 {"from":"junction","to":"openspace","distance":14,"obstacle_classes":["chair"]},
 {"from":"junction","to":"studyarea","distance":15,"obstacle_classes":["table"]},
 {"from":"openspace","to":"meetingroom","distance":14,"obstacle_classes":["chair","table"]},
 {"from":"studyarea","to":"meetingroom","distance":13,"obstacle_classes":["chair"]},
 {"from":"openspace","to":"studyarea","distance":20,"obstacle_classes":[]},
]
