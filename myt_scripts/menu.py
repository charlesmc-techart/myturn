import nuke


def set_project_frame_range(read_node: str = "Read1"):
    read_node = nuke.toNode(read_node)
    first_frame = read_node["origfirst"].getValue()
    last_frame = read_node["origlast"].getValue()

    project_settings = nuke.root()
    project_settings["first_frame"].setValue(first_frame)
    project_settings["last_frame"].setValue(last_frame)


def sfr(read_node: str = "Read1"):
    set_project_frame_range(read_node)


## nuke.addOnCreate(set_project_frame_range, nodeClass="Read")
