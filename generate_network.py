import xml.etree.ElementTree as ET
from xml.dom import minidom
import subprocess
import json


def write_xml(root,filename):
    with open(filename, "w", encoding="utf-8") as file:
        xml_content = minidom.parseString(ET.tostring(root, encoding="utf-8")).toprettyxml(indent="    ")
        file.seek(0)
        file.truncate()
        file.write(xml_content)

def set_attr(Dicts,root,name):
    for dt in Dicts:
        element = ET.SubElement(root, name)
        for key,value in dt.items():
            element.set(key,value)


def generate_nodes(roadnet,filename):
    nodes=[]
    intersections=roadnet['intersections']
    for inter in intersections:
        nodes.append({
        'id':inter['id'],
        'x':str(inter['point']['x']),
        'y':str(inter['point']['y']),
        'type':"traffic_light",
        })

    root = ET.Element("nodes")
    set_attr(nodes,root,name='node')
    write_xml(root,filename)


def generate_edges(roadnet,filename):
    edges=[]
    roads=roadnet['roads']
    for edge in roads:
        from_=edge['startIntersection']
        to=edge['endIntersection']
        ID='road_'+from_.split('_')[1]+'_'+to.split('_')[1]   # +f"_{len(edge['lanes'])}"
        points= edge['points']
        xy = f"{points[0]['x']},{points[0]['y']} {points[1]['x']},{points[1]['y']}"
        
        lanes=[]
        lanes_info=edge['lanes']
        for i,lane in enumerate(lanes_info):
            lanes.append({
                'index':str(i),
                'speed':str(lane['maxSpeed']),
                'width':str(lane['width'])
                })

        edges.append({
            'id':ID,
            'from':from_,
            'to':to,
            'shape':xy,
            'numLanes':str(len(edge['lanes'])),
            'lanes':lanes,
        })

    root = ET.Element("edges")
    for edge in edges:
        edge_element = ET.SubElement(root, "edge")
        lanes_=edge.pop('lanes')
        for key,value in edge.items():
            edge_element.set(key,value)

        lane_element=ET.SubElement(edge_element, "lane")
        for lane in lanes_:
            for key,value in lane.items():
                lane_element.set(key,value)
                
    write_xml(root,filename)


def generate_connections(roadnet,filename):
    connections=[]
    intersections=roadnet['intersections']
    for inter in intersections:
        roadlinks=inter['roadLinks']
        for link in roadlinks:
            from_=link['startRoad']
            to=link['endRoad']
            for lak in link['laneLinks']:
                connections.append({
                    'from':from_,
                    'to':to,
                    'fromLane':str(lak['startLaneIndex']),
                    'toLane':str(lak['endLaneIndex']),
                })

    root = ET.Element("connections")
    set_attr(connections,root,name='connection')
    write_xml(root,filename)


def generate_types(filename):
    raise NotImplementedError


def convert_xml_to_netxml(file_nodes,file_edgs,file_connections, netxml_file_path):
    try:
        command = [
            "netconvert",
            "-n", file_nodes,
            "-e", file_edgs,
            "-c", file_connections,
            "-o", netxml_file_path]
        subprocess.run(command, check=True)
        print("Conversion successful.")

    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")












