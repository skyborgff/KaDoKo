def getClass(node_list, check_class):
    matches = []
    node_matches = []
    for node in node_list:
        raw_node = node["info"]["raw"]
        if type(raw_node) == check_class:
            matches.append(raw_node)
            node_matches.append(node["hash"])
    return matches, node_matches


def dump_info(node_hashes, database):
    info_dump = []
    for hash in node_hashes:
        info = database.graph.nodes[hash]
        info_dump.append({"info": info, "hash": hash})
    return info_dump


def simpleAdd(AnimeInfo, node_list):
    info, node_hash = getClass(node_list, type(AnimeInfo))
    if info:
        return info[0]
    return AnimeInfo