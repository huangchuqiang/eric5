import xml.etree.ElementTree as ET
import sys, os

# 属性比较
def compare_attr(dictattr1,  dictattr2):
    dictvalue = {}
    # dictattr1 - dictattr2
    diffLis = dictattr1.keys() - dictattr2.keys()
    print (diffLis)
    for item in diffLis:
        dictvalue[item] = "only ({0}) exist attrib".format(os.path.split(sys.argv[1])[1])
    # dictattr2 - dictattr1    
    diffLis = dictattr2.keys() - dictattr1.keys()
    print (diffLis)
    for item in diffLis:
        dictvalue[item] = "only ({0}) exist attrib".format(os.path.split(sys.argv[2])[1])
    
    # dictattr2 & dictattr1 
    andList = dictattr1.keys() & dictattr2.keys()
    #print (andList)
    for key in andList:
        if dictattr1[key] != dictattr2[key]:
            dictvalue[key] = "different_value({0})and({1})".format(dictattr1[key],  dictattr2[key])
    return dictvalue        
   
def getAttribute(node):
    if node == None:
        return dict()
    else:
        return node.attrib

def getChildren(node):
    if node == None:
        return list()
    else:
        return node.getchildren()
        
#节点比较
def compare_xmltree(root1, root2, domTree,  xmlNode):        
    dictvalue = compare_attr(getAttribute(root1),  getAttribute(root2))
    if len(dictvalue) > 0:
        for k,  v in dictvalue.items():
            xmlNode.setAttribute(k,  v)    
    #取孩子结点
    childrenlist1 = getChildren(root1)
    childrenlist2 = getChildren(root2)
    print (childrenlist1)
    print (childrenlist2)    
    list1 = [child.tag for child in childrenlist1]
    list2 = [child.tag for child in childrenlist2]
    set1 = set(list1)
    set2 = set(list2)
    
    diffSet = set1 - set2
    print (diffSet)
    for item in diffSet:
        index = list1.index(item)
        childnode = domTree.createElement(item)
        compare_xmltree(childrenlist1[index],  None,  domTree,  childnode)
        if childnode.hasAttributes() or childnode.hasChildNodes():
            xmlNode.appendChild(childnode)
            
    diffSet = set2 - set1
    print (diffSet)
    for item in diffSet:
        index = list2.index(item)
        childnode = domTree.createElement(item)
        compare_xmltree(None,  childrenlist2[index],  domTree,  childnode)
        if childnode.hasAttributes() or childnode.hasChildNodes():
            xmlNode.appendChild(childnode)
    
    diffSet = set2 & set2
    print (diffSet)
    for item in diffSet:
        index1 = list1.index(item)
        index2 = list2.index(item)
        childnode = domTree.createElement(item)
        compare_xmltree(childrenlist1[index1],  childrenlist2[index2],  domTree,  childnode)
        if childnode.hasAttributes() or childnode.hasChildNodes():
            xmlNode.appendChild(childnode)
    return True

if __name__ == "__main__":
    from xml.dom import  minidom
    tree1 = ET.parse(sys.argv[1])
    tree2 = ET.parse(sys.argv[2])
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    if root1.tag != root2.tag:
        print ("两个xml文件的根结点不同，不能比较")
        sys.exit(0)
    #生成domTree
    impl = minidom.getDOMImplementation()
    dom = impl.createDocument(None, None, None)
    
    #i添加节点
    root = dom.createElement(root1.tag)    
    compare_xmltree(root1, root2, dom, root)
    if root.hasAttributes() or root.hasChildNodes():
        dom.appendChild(root)
    
    save2file = ""
    if sys.argv[3][1] == ":":
        save2file = sys.argv[3]
    else:
        save2file = os.getcwd() + "\\" + sys.argv[3]
        
    file = open(save2file,  "w",  encoding = 'UTF8')
    dom.writexml(file,  "","\t",  "\n",  "utf-8")
    file.close()
    print ("succeed exit")
