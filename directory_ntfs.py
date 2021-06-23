from partition_boot_sector_ntfs import *

class Node():
    def __init__(self,entry =None,parent = None, id=None):
        #type = entry
        self.entry = entry
        self.parent = parent # node
        self.ID = id
        self.childs = []
    def getProperty(self):
        return self.entry.getPropertyEntry()
    def isEmpty(self):
        return self.entry == None
    def addChildren(self,child):
        self.childs.append(child)
    def isDirectory(self):
        return self.entry.is_directory()
    def getChildrenList(self):
        return self.childs
    def getFileName(self):
        return self.entry.getFileName()
    def getID(self):
        return self.ID
    def getPath(self):
        return self.entry.getPath()
    def getParent(self):
        return self.parent

class Root():
    def __init__(self,directory):
        self.directory = directory
        self.root = Node()
        self.entries = [self.root]
        self.addRoot()
        self.addSRoot(self.root)
        self.transfer(self.root)
    def addRoot(self):
        for i in range(1, len(self.directory)):
            if self.directory[i].parent_ID==5 and self.directory[i].is_in_use():
                self.root.addChildren(Node(self.directory[i], self.root, self.directory[i].getID()))
                # print(self.directory[i].fname_str)
    def addSRoot(self,root):
        # print(len(root.getChildrenList()))
        if (len(root.getChildrenList()) > 0):
            childs = root.getChildrenList()
            for child in childs:
                if child.isDirectory():
                    # print(child.entry.fname_str)
                    for i in range(1, len(self.directory)):
                        if child.getID() == self.directory[i].parent_ID and self.directory[i].is_in_use():
                            child.addChildren(Node(self.directory[i],child,self.directory[i].getID()))
                            # print(self.directory[i].fname_str)
                    self.addSRoot(child)
                    # child2=child.getChildrenList()
                    # for v in child2:
                    #     if v.isDirectory():
                    #         print(v.ID)
                    #         self.addSRoot(v)
    def insertNode(self,root,entry):
        if (not root.isEmpty()):
            if root.getPath() + "/" + entry.getFileName() == entry.getPath() :
                return root.addChildren(Node(entry, root))
        if (len(root.getChildrenList()) > 0):
            childs = root.getChildrenList()
            for child in childs:
                if child.isDirectory():
                        self.insertNode(child,entry)
    def transfer(self,root):
        if (len(root.getChildrenList()) > 0):
            childs = root.getChildrenList()
            for child in childs:
                self.entries.append(child)
                # print(child.getFileName())
                if child.isDirectory():
                    self.transfer(child)
        return
    def getNodeList(self):
        return self.entries
    def getRoot(self):
        return self.root