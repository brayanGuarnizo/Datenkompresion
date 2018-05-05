# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 18:56:50 2018
http://www.openbookproject.net/py4fun/huffman/huffman.html
@author: Gunnydo
"""
import numpy

codes={}
 
def frequency (list) :
    freqs = {}
    for ch in list :
        freqs[ch] = freqs.get(ch,0) + 1
    return freqs

def sortFreq (freqs) :
    letters = freqs.keys()
    #print(sorted(letters))
    tuples = []
    #for  value in sorted(letters):
    for let in sorted(letters) :
        tuples.append((freqs[let],let))
    tuples.sort()
    return tuples


def buildTree(tuples) :
    while len(tuples) > 1 :
        leastTwo = tuple(tuples[0:2])                  # get the 2 to combine
        theRest  = tuples[2:]                          # all the others
        combFreq = leastTwo[0][0] + leastTwo[1][0]     # the branch points freq
        tuples   = theRest + [(combFreq,leastTwo)]     # add branch point to the end
        #tuples.sort()                                  # sort it into place
    return tuples[0]            # Return the single tree inside the list

def trimTree (tree) :
     # Trim the freq counters off, leaving just the letters
    #print(p)
    
    #print("tree",type(tree),type((1,1)))
    if type(tree)==type((1,1)):
        #print("type1",type(tree[1]))
        if(type(tree[1]))==type((1,1)):
            p = tree[1]
            return (trimTree(p[0]), trimTree(p[1]))
        else:
            return tree
        #print("huhu")
        ##print(p)
        #print(type(p))                                  # ignore freq count in [0]
    else:
        return tree              # if just a leaf, return it
    #else : return (trimTree(p[0]), trimTree(p[1])) # trim left then right and recombine

def assignCodes (node, pat='') :
   
    if type(node) == type((1,1)) :
        #codes[node] = pat                # A leaf. set its code
        if type(node[0]) == type((1,1)):
            
            assignCodes(node[0], pat+"0")    # Branch point. Do the left branch
            assignCodes(node[1], pat+"1")
        else:
            codes[node]=pat
    else  :                              #
        #assignCodes(node[0], pat+"0")    # Branch point. Do the left branch
        #assignCodes(node[1], pat+"1")    # then do the right branch.
        codes[node] = pat
        
        
def encode (stri) :
    #print("Code: ",codes)
    output = ""
    for ch in stri :
        output += codes[ch]
        
    return output

def decode (tree, str) :
    output = []
    p = tree
    for bit in str :
       # print(bit)
        if bit == '0' : p = p[0]     # Head up the left branch
        else          : p = p[1]
       # print(p, type(p),type(p[0]),type(p[1]))# or up the right branch
        if type(p) == type((1,1)) and type(p[0])==type(1):
            output.append(p)
           # print("output",output)              # found a character. Add to output
            p = tree                 # and restart for next character
    return output

# =============================================================================
# freqs = frequency(["(a)","(a)","(a)","(b)","(c)","(c)","(d)","(e)","(e)","(e)","(e)","(e)","(f)","(f)","(g)"])
# print(freqs)
# tuples = sortFreq(freqs)
# print(tuples)
# tree = buildTree(tuples)
# print(tree)
# trim = trimTree(tree)
# print(trim)
# assignCodes(trim)
# print(codes)
# encoded=encode(["(a)","(a)","(a)","(b)","(c)","(c)","(d)","(e)","(e)","(e)","(e)","(e)","(f)","(f)","(g)"])
# print(encoded)
# decoded=decode(trim,encoded)
# print(decoded)
# =============================================================================
