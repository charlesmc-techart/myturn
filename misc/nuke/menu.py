# type: ignore

import nuke


def setProjectFrameRange(readNode: str = "Read1") -> None:
    """Set the project's frame range based on Read1's orig frame range"""
    readNode = nuke.toNode(readNode)
    firstFrame = readNode["origfirst"].getValue()
    lastFrame = readNode["origlast"].getValue()

    projectSettings = nuke.root()
    projectSettings["first_frame"].setValue(firstFrame)
    projectSettings["last_frame"].setValue(lastFrame)


def sfr(readNode: str = "Read1") -> None:
    """Shorthand wrapper for interactive scripting"""
    setProjectFrameRange(readNode)


# nuke.addOnCreate(setProjectFrameRange, nodeClass="Read")
