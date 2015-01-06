
def RenderSetup():
    ResetRenderState()
    AddSelectIndex()
    AddRenderNode()

def SetupNode():
    pass
    
def AddSelectIndex():
    root_node = hou.node("./INDEX")
    context = hou.node(".")

    for i in xrange(hou.ch("rotation_range")):
        del_node = context.createNode("delete", "DEL_INDEX_" + str(i))
        del_node.setParms({"group": "index" + str(i), "negate": 1})
        nul_node = context.createNode("null", "INDEX_" + str(i))
        del_node.setFirstInput(root_node)
        nul_node.setFirstInput(del_node)
    context.layoutChildren()



def AddRenderNode():
    root_node = hou.node("./render/root")
    context = hou.node("./render")
    merge = hou.node("./render/merge")
    
    for i in xrange(hou.ch("rotation_range")):
        geo_node = context.createNode("geometry", "RENDER_" + str(i))
        geo_node.setParms({"soppath": "../../INDEX_" + str(i), "mkpath": 1, "sopoutput": "$HIP/objectArray/output_" + str(i) + "_$F.bgeo", "trange": 2, "f1": -hou.ch("bend_range")/2, "f2": hou.ch("bend_range")/2})
        geo_node.setFirstInput(root_node)
        merge.setNextInput(geo_node)
    context.layoutChildren(root_node.outputs())

def ResetRenderState():
    root_node = hou.node("./render/root")
    merge = hou.node("./render/merge")
    context = hou.node("./render")
    for node in root_node.outputs():
        node.destroy()
    merge.setInput(0,None)
    root_node = hou.node("./INDEX")
    context = hou.node(".")
    for node in root_node.outputs():
        for out in node.outputs():
            out.destroy()
        node.destroy()
