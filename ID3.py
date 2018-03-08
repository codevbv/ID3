#Luis Solorzano
#ID3.py
import sys
import random
import math

# print out the tree by going through each node and then through its children
def printTree(root,count):
    M= root
    for i in range(count):
        print(" ", end="")
    print(M.attribute)
    for key,value in M.children.items():
        print(" ", end="")
        for i in range(count):
            print(" ", end="")
        print(value,end=" ")
        if M.children[value].label != "":
            print(M.children[value].attribute)
            printTree(M.children[value], count+2)

#determines the mostCommmonLabel for a given instance set
def mostCommonLabel(instanceSet):
    count={}
    for i in instanceSet:
        if i.getLabel() in count:
            count[i.getLabel()]+=1
        else:
            count[i.getLabel()]=1

    most= -1
    mostLabel=""
    for key, vals in count.items():
        if int(vals) > most:
            mostLabel=key
            most=vals
    return mostLabel

#finds the most common label out of our instance set
#by going through the instanceObjects
def mostCommon(instanceSet):
    commonList= []
    for inst in instanceSet:
        found =0
        for i in range(0,len(commonList)):
            if commonList[i][0]== inst.label:
                commonList[i][1]+=1
                found=1
        if found ==0:
            commonList.append([inst.label,1])
    commonList.sort(key=lambda tup: tup[1],reverse=True)
    return commonList[0][0]

#calculates the randomness in the instanceSet
def entropy(instanceSet):
    H=0
    count={}
    for i in instanceSet:
        if i.label in count:
            count[i.label]+=1
        else:
            count[i.label]=1.0
    for key,vals in count.items():
        yProportion= float(vals/len(instanceSet))
        H-= yProportion * math.log(yProportion,2)
    return H

#calculate the gain for an attribute out of the entire instanceSet
def gain(instanceSet,attribute):
    summ=0
    H= entropy(instanceSet)
    count={}
    for i in instanceSet:
        if i.getAttribute(attribute) in count:
            count[i.getAttribute(attribute)]+=1
        else:
            count[i.getAttribute(attribute)]=1.0
    for key,vals in count.items():
        Sv=[]
        for i in instanceSet:
            if i.getAttribute(attribute)== key:
                Sv.append(i)
        proportion= len(Sv)/len(instanceSet)
        HSv= entropy(Sv)
        H-= proportion*HSv
    return H   

#checks to see if labels in an instanceSet are all the same 
def allSameLabel(instanceSet):
    label= instanceSet[0].getLabel() #grabs first label
    for i in instanceSet:
        if i.getLabel() != label:
            return False
    return True

#takes in a set, the most common label for that set, and then list of possible attributes
# and attributeDict is a dictionary for all the attributes with their possible values
def ID3(instanceSet,mostCommonLabel,attributeNames,attributeDict):
    if len(attributeNames)==0: #empty dictionaries evalute to false
        node= TreeNode()
        node.addLabel(mostCommonLabel)
    #all have same label
    elif(allSameLabel(instanceSet)):
        node= TreeNode()
        node.addLabel(mostCommonLabel)
    #find a*
    else:
        a=-100000
        aName= None
        for i in attributeNames:
            otherA=gain(instanceSet,i)
            if otherA>a:
                a=otherA
                aName=i
        node= TreeNode() #non leaf node
        node.addAttribute(aName) #with attribute a*
        aVals=attributeDict[aName]
        node.addChildren(aVals)
    #partition set into subsets Sv
        for v in aVals:
            Sv=[]
            for j in instanceSet:
                if j.dict[aName]==v:
                    Sv.append(j)
            if len(Sv)==0:
                node.children[v].addLabel(mostCommon(instanceSet))
            else:
                newAttributeNames=[]
                for a in attributeNames:
                    if a != aName:
                        newAttributeNames.append(a)
                
                mcl=mostCommon(Sv)
                node.children[v]= ID3(Sv,mcl,newAttributeNames,attributeDict)    
    return node
            
        
        
    

#an object for each instance that holds its attributes and
#tells whether or not it is a labeled
class instanceObject:
    
    def __init__(self,label,):
        self.dict={}
        self.label=label

    def add_attributes(self,attributes,vals):
        for i in range(0,len(attributes)):
            self.dict[attributes[i]]=vals[i]

    def getLabel(self):
        return self.label

    def getAttribute(self,attribute):
        return self.dict[attribute]
    
    def __str__(self):
        string=self.label
        string+='\n'
        for key, vals in self.dict.items():
            string+= key
            string+=": "
            string+=vals
            string+='\n'
        return string 


#generic tree node class
class TreeNode:

    def __init__(self):
        self.children=None
        self.leaf=True
        self.attribute=None
        self.label=""

    def addLabel(self,label):
        self.label=label

    def isLeaf(self):
        return self.leaf
    
    def addAttribute(self,attribute):
        self.attribute=attribute

    def getAttribute(self):
        return self.attribute

    def getLabel(self):
        return self.label

    def addChildren(self,values):
        self.children={}
        for value in values:
            self.children[value]=TreeNode()
        self.leaf=False
        
        
    
def main():
    
    dataSet=sys.argv[1]
    percent= eval(sys.argv[2])
    seed=eval(sys.argv[3])
    file= open(dataSet,"r")
    count=0 #skip the first row
    random.seed(seed)
    instances=[]
    labels= set()
    attributeDict={} #keys are attributes and values are the possible values for the attributes
    for line in file:
        splitLine=line.strip()
        splitLine= splitLine.split(",")
        
        if count == 0:
            attributeNames=splitLine[1:]
            count+=1
            for i in attributeNames:
                attributeDict[i]=set()#make key for attribute names
            continue

        count+=1
        labels.add(splitLine[0])
        label=splitLine[0]
        attributes=splitLine[1:]
        inst= instanceObject(label)
        inst.add_attributes(attributeNames,attributes)
        instances.append(inst)
        for i in range(0,len(attributes)):
            attributeDict[attributeNames[i]].add(attributes[i])
    
#randomize dataset instances into a testset and a trainingSet which is based off
#the percentage that the user gives            
    random.shuffle(instances) 
    testSet=[]
    trainingSet=[]
    

    for i in range(0,int(count*percent)):
        trainingSet.append(instances[i])

    for j in range(int(count*percent),count-1):
        testSet.append(instances[j])

    trainingMCL=mostCommon(trainingSet)
    root=ID3(trainingSet,trainingMCL,attributeNames,attributeDict)#feed trainingSet into ID3

    predictions={}

    for i in testSet:
        done=False
        predictionLabel=""
        testRoot=root #copy root to testRoot
        while not done:
            if testRoot.isLeaf():
                predictionLabel=testRoot.label
                done = True
            else:
                val= i.dict[testRoot.attribute]
                testRoot= testRoot.children[val]
        matrixRep=("%s,%s" %(i.label,predictionLabel))
        if matrixRep in predictions.keys():
            predictions[matrixRep] +=1
        else:
            predictions[matrixRep]=1

#Printing a confusion matrix for our predictions on testSet
#this is the outputted to the current directory as a csv file
#if user makes "python3 ID3.py monks1.csv 0.75 12345", then the
#output file will be titled 'results_ID3_monk1.csv_12345.csv'
    Fname = ("results_ID3__%s__%d.csv" %(dataSet,seed))
    F= open(Fname,"w")
    correct=0
    total=0
    for l in labels:
        F.write("%s,"%(l))
    F.write("\n")
    for l in labels:
        for i in labels:
            matrixRep=("%s,%s" %(l,i))
            if matrixRep in predictions.keys():
                num= predictions[matrixRep]
                if l ==i:
                    correct+=num
                total += num
                F.write("%d,"%(num))
            else:
                F.write("0,")
        F.write(l+ "\n")
    F.close()
    confidence= correct/total
    print(confidence,end=",")
    #printTree(root,0)
    
        
    



main()
