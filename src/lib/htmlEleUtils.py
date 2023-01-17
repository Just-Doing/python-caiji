def getNodeText(node):
    if(node == None):
        return ""
    else:
        return node.get_text().strip()

def getInnerHtml(node):
    if(node == None):
        return ""
    else:
        return node.prettify()
