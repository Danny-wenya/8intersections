import json
from generate_flow import *
from generate_network import *



if __name__=="__main__":

    # generate flow
    flows = json.load(open('./SH2/flow.json', 'rb'))
    root = ET.Element('routes')
    vTypes, routes, vehicles = generate_rou_element(flows)

    set_elements_attr(root, vTypes, 'vType')
    set_elements_attr(root, routes, 'route')
    set_elements_attr(root, vehicles, 'vehicle')

    filename = './SH2.rou.xml'
    write_xml(root, filename)


    # generate network
    roadnet = json.load(open('./SH2/roadnet.json', 'r'))
    file_nodes,file_edgs,file_connections='./SH2.nod.xml', './SH2.edg.xml', './SH2.con.xml'
    netxml_file_path = "./SH2.net.xml"

    generate_nodes(roadnet,file_nodes)
    generate_edges(roadnet,file_edgs)
    generate_connections(roadnet,file_connections)
    # generate_types(file_types)

    convert_xml_to_netxml(file_nodes,file_edgs,file_connections, netxml_file_path)