import re

class Node(object):

    # A Node with list of Nodes as subtree, Single Node as a parent
    def __init__(self, val='', parent=None, inval=None):
        self.val = val        # name of the Node
        self.subtrees = []    # list of subtree Node objects
        self.parent = parent  # parent of the Node
        self.inval = inval    # content of the tag is stored

    # returns matching Node in given Node and its immediate children
    def level_search(self, Node, key):
        if Node.val == key:
            return Node
        else:
            for subtree in Node.subtrees:
                if subtree.val == key:
                    return subtree


def create_listofwords(xml):
    listofwords = []
    xml = re.sub('\t', ' ', xml)
    xml = re.sub(' +', ' ', xml)  # compress multiple spaces
    print(xml)

    for index, character in enumerate(xml):
        if character == '<':
            runningtag = True
            opentagindex = index
        elif character == '>':
            closetagindex = index
            listofwords.append(xml[opentagindex:closetagindex+1])

            runningtag = False
        else:
            if runningtag == False and xml[index-1] == '>':
                opentagindex = index
            elif runningtag == False and xml[index+1] == '<':
                closetagindex = index
                listofwords.append(xml[opentagindex:closetagindex+1])

    # remove words consisting of only whitespaces
    while ' ' in listofwords:
        listofwords.remove('  ')

    if listofwords[0][0] == '<' and listofwords[0][1] == '?':
        del listofwords[0]

    # print('\n',listofwords)
    return listofwords

# bulid the tree from given xml data
def build_tree(xml):

    listofwords = create_listofwords(xml)

    tag = []     # stack used to keep track of opening and closing tags
    pointing_Node = None  # pointer used to keep track of insertion point
    for j, i in enumerate(listofwords):

        if i[0] == '<' and i[1] != '/':  # if the element is opening tag

            if pointing_Node != None:
                temp = Node(i[1:len(i)-1])
                pointing_Node.subtrees.append(temp)
                temp.parent = pointing_Node  # adding the Node to the tree

                pointing_Node = temp
                tag.append(i)  # push the Node on tagstack

            else:
                temp = Node(i[1:len(i)-1])
                pointing_Node = temp
                if pointing_Node.parent != None:
                    origin = pointing_Node.parent
                else:
                    origin = pointing_Node
                tag.append(i)

        elif i[0] == '<' and i[1] == '/':  # if the element is closing tag
            if len(tag) > 0:
                pointing_Node = pointing_Node.parent  # point to the parent
                tag.pop()  # pop the tagstack

        else:  # if the element is content of the tag

            if pointing_Node != None:
                pointing_Node.inval = i
                # print(pointing_Node.val,)
    return origin


# searches the tree bulit for the given path
def search_path(pathgiven, origin):

    # split the string with '/' as a delimitor and ignore first element as it is ''
    path = pathgiven.split('/')[1:]
    pl = len(path)
    pointing_Node = origin
    
    for index, name in enumerate(path):  # search for each word in the path
        if index < pl and pointing_Node != None:
            if pointing_Node.subtrees != []:
                # print(pointing_Node.val,name)
                pointing_Node = pointing_Node.level_search(pointing_Node, name)
            else:
                print('\nresult for the given query \"' +
                      pathgiven + '\" is\n'+" given path is incorrect")
                return

    if hasattr(pointing_Node, 'inval'):
        print('\nresult for the given query \"' +
              pathgiven + '\" is\n', pointing_Node.inval)
    else:
        print('\nresult for the given query \"' +
              pathgiven + '\" is\n'+" given path is incorrect")


def main():
    # read xml file and build tree
    with open('person.xml', 'r') as myfile:
        xml = myfile.read().replace('\n', '')
    origin = build_tree(xml)

    # test case1
    pathgiven = '/person/address/street'
    search_path(pathgiven, origin)

    # test case2 (wrong path)
    pathgiven = '/person/name/address'
    search_path(pathgiven, origin)

    # test case3(incomplete path)
    pathgiven = '/person/street'
    search_path(pathgiven, origin)

    # test case 4(complete path with no value inside )
    pathgiven = '/person/address/postcode'
    search_path(pathgiven, origin)

    # xml with name with same tags
    with open('country.xml', 'r') as myfile:
        xml = myfile.read().replace('\n', '')
    origin = build_tree(xml)

    pathgiven = '/country/state/capital'
    search_path(pathgiven, origin)

    pathgiven = '/country/Union_Territory/capital'
    search_path(pathgiven, origin)

    with open('note.xml', 'r') as myfile:
        xml = myfile.read().replace('\n', '')
    origin = build_tree(xml)

    pathgiven = '/note/heading'
    search_path(pathgiven, origin)


if __name__ == "__main__":
    main()
