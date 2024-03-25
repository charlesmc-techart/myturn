import nuke


def setProjectFrameRange(readNode: str = "Read1"):
    readNode = nuke.toNode(readNode)
    firstFrame = readNode["origfirst"].getValue()
    lastFrame = readNode["origlast"].getValue()

    projectSettings = nuke.root()
    projectSettings["first_frame"].setValue(firstFrame)
    projectSettings["last_frame"].setValue(lastFrame)


def sfr(readNode: str = "Read1"):
    setProjectFrameRange(readNode)


# nuke.addOnCreate(setProjectFrameRange, nodeClass="Read")
