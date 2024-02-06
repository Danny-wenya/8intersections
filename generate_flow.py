# 先观察路网文件
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import subprocess

def generate_rou_element(flows):
    vTypes = []
    routes = []
    vehicles = []
    v, r = 0, 0
    v_index, r_index = [], []

    for i, flow in enumerate(flows):
        # vtype
        vehicle = flow['vehicle']
        vType = {
            'width': '2',
            'length': '5',
            'sigma': '0.5',
            'color': "1,0,0",
            'minGap': f"{vehicle['minGap']}",
            'tau': f"{vehicle['headwayTime']}",
            'maxSpeed': f"{vehicle['maxSpeed']}",
            'accel': f"{vehicle['usualPosAcc']}",
            'decel': f"{vehicle['usualNegAcc']}",
            'emergencyDecel': f"{vehicle['maxNegAcc']}",
        }
        if vType not in vTypes:
            vTypes.append(vType)
            vi='vType' + f'{v}'
            v_index.append(vi)
            v += 1

        # route
        route = {
            'edges': ' '.join(flow['route']),
        }
        if route not in routes:
            routes.append(route)
            ri='route' + f'{r}'
            r_index.append(ri)
            r += 1

        # vehicle
        vehicles.append({
            'id': 'veh' + f'{i}',
            'type': vi,
            'route': ri,
            'depart': f"{flow['startTime']}",
        })

    for Type, v_idx in zip(vTypes, v_index):
        Type['id'] = v_idx

    for route, r_idx in zip(routes, r_index):
        route['id'] = r_idx

    return vTypes, routes, vehicles


def set_elements_attr(root, types, element_name):
    for type in types:
        types_element = ET.SubElement(root, element_name)
        for key, value in type.items():
            types_element.set(key, value)


def write_xml(root, filename):
    with open(filename, "w", encoding="utf-8") as file:
        xml_content = minidom.parseString(ET.tostring(root, encoding="utf-8")).toprettyxml(indent="    ")
        file.seek(0)
        file.truncate()
        file.write(xml_content)


