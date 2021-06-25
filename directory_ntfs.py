class NodeNTFS():
    def __init__(self,entry =None,parent = None, id=None, path="", name=""):
        path+="\\"
        self.path = path+name
        self.entry = entry
        self.parent = parent # node
        self.ID = id
        self.childs = []
    def getProperty(self):
        return self.entry.getProperties()
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
        return self.path
    def getParent(self):
        return self.parent

class RootNTFS():
    def __init__(self,directory,path):
        self.directory = directory
        self.root = NodeNTFS(path=path)
        self.entries = [self.root]
        self.addRoot(path)
        self.addSRoot(self.root)
        self.transfer(self.root)
    def addRoot(self,path):
        for i in range(1, len(self.directory)):
            if self.directory[i].parent_ID==5 and self.directory[i].is_in_use():
                self.root.addChildren(NodeNTFS(self.directory[i], self.root, self.directory[i].getID(),path,self.directory[i].getFileName()))
    def addSRoot(self,root):
        if (len(root.getChildrenList()) > 0):
            childs = root.getChildrenList()
            for child in childs:
                if child.isDirectory():
                    for i in range(1, len(self.directory)):
                        if child.getID() == self.directory[i].parent_ID and self.directory[i].is_in_use():
                            child.addChildren(NodeNTFS(self.directory[i],child,self.directory[i].getID(), child.getPath(),self.directory[i].getFileName()))
                    self.addSRoot(child)
    def transfer(self,root):
        if (len(root.getChildrenList()) > 0):
            childs = root.getChildrenList()
            for child in childs:
                self.entries.append(child)
                if child.isDirectory():
                    self.transfer(child)
    def getNodeList(self):
        return self.entries
    def getRoot(self):
        return self.root
    def getPropertyFromPath(self, path):
        property = ""
        for v in self.entries[1:]:
            if v.getPath()[4:] == path:
                property = "\nPath: " + v.getPath()[4:] +v.getProperty()
                break
        return property