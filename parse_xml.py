#!/usr/bin/env python
# coding: utf-8



import re


class node(object):

    # A node with list of nodes as subtree, Single node as a parent
    def __init__(self, val='', parent=None, inval=None):
        self.val = val        # name of the node
        self.subtrees = []    # list of subtree node objects
        self.parent = parent  # parent of the node
        self.inval = inval    # content of the tag is stored



    # returns matching node in given node and its immediate children
    def level_search(self, node, key):
        if node.val == key:
            return node
        else:
            for subtree in node.subtrees:
                if subtree.val == key:
                    return subtree




def create_listofwords(xml):
    listofwords = []
    xml = re.sub('\t', ' ', xml)
    xml = re.sub(' +', ' ', xml) #compress multiple spaces
    print(xml)

    #
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
                
    #remove words consisting of only whitespaces
    while ' ' in listofwords:
        listofwords.remove('  ')
    if listofwords[0][0] == '<' and listofwords[0][1] == '?':
        del listofwords[0]
    #print('\n',listofwords)
    return listofwords

# bulid the tree from given xml data
def build_tree(xml):

    
    

 
    listofwords=create_listofwords(xml)

    tag = []     # stack used to keep track of opening and closing tags
    pointing_node = None  # pointer used to keep track of insertion point
    for j, i in enumerate(listofwords):

        if i[0] == '<' and i[1] != '/':  # if the element is opening tag

            if pointing_node != None:
                temp = node(i[1:len(i)-1])
                pointing_node.subtrees.append(temp)
                temp.parent = pointing_node  # adding the node to the tree

                pointing_node = temp
                tag.append(i)  # push the node on tagstack

            else:
                temp = node(i[1:len(i)-1])
                pointing_node = temp
                if pointing_node.parent != None:
                    origin = pointing_node.parent
                else:
                    origin = pointing_node
                tag.append(i)

        elif i[0] == '<' and i[1] == '/':  # if the element is closing tag
            if len(tag) > 0:
                pointing_node = pointing_node.parent  # point to the parent
                tag.pop()  # pop the tagstack

        else:  # if the element is content of the tag

            if pointing_node != None:
                pointing_node.inval = i
                # print(pointing_node.val,)
    return origin




#searches the tree bulit for the given path
def search_path(pathgiven,origin):
    
    path = pathgiven.split('/')[1:]   #split the string with '/' as a delimitor and ignore first element as it is ''
    pl = len(path)
    pointing_node = origin
    for index, name in enumerate(path):  #search for each word in the path
        if index < pl and pointing_node != None:
            if pointing_node.subtrees != []:
                # print(pointing_node.val,name)
               pointing_node = pointing_node.level_search(pointing_node, name)
            else:
               print('\nresult for the given query \"'+ pathgiven +'\" is\n'+" given path is incorrect")
               return 
	    


    if hasattr(pointing_node, 'inval'):
        print('\nresult for the given query \"'+ pathgiven +'\" is\n', pointing_node.inval)
    else:
         print('\nresult for the given query \"'+ pathgiven +'\" is\n'+" given path is incorrect")



#read xml file and build tree
with open('person.xml', 'r') as myfile:
    xml= myfile.read().replace('\n', '')
origin = build_tree(xml)


#test case1
pathgiven = '/person/address/street'
search_path(pathgiven,origin)

#test case2 (wrong path)
pathgiven = '/person/name/address'
search_path(pathgiven,origin)

#test case3(incomplete path)
pathgiven = '/person/street'
search_path(pathgiven,origin)


#test case 4(complete path with no value inside )
pathgiven = '/person/address/postcode'
search_path(pathgiven,origin)



# xml with name with same tags
with open('country.xml', 'r') as myfile:
    xml= myfile.read().replace('\n', '')
origin = build_tree(xml)


pathgiven = '/country/state/capital'
search_path(pathgiven,origin)


pathgiven = '/country/Union_Territory/capital'
search_path(pathgiven,origin)


with open('note.xml', 'r') as myfile:
    xml= myfile.read().replace('\n', '')
origin = build_tree(xml)


pathgiven = '/note/heading'
search_path(pathgiven,origin)



