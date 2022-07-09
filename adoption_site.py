import os
from xml.dom import IndexSizeErr
from forms import  AddForm , DelForm
from flask import Flask, render_template, url_for, redirect,request
from csv import writer
import csv

"""Simple implementation of a B+ tree, a self-balancing tree data structure that (1) maintains sort
data order and (2) allows insertions and access in logarithmic time.
"""
global f
global result
result=[]

global keys_at_each_level

class Node(object):
    """Base node object.
    Each node stores keys and values. Keys are not unique to each value, and as such values are
    stored as a list under each key.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order):
        """Child nodes can be converted into parent nodes by setting self.leaf = False. Parent nodes
        simply act as a medium to traverse the tree."""
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def add(self, key, value):
        """Adds a key-value pair to the node."""
        # If the node is empty, simply insert the key-value pair.
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            # If new key matches existing key, add to list of values.
            if key == item:
                self.values[i].append(value)
                break

            # If new key is smaller than existing key, insert new key to the left of existing key.
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            # If new key is larger than all existing keys, insert new key to the right of all
            # existing keys.
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])

    def split(self):
        """Splits the node into two and stores them as child nodes."""
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        # When the node is split, set the parent key to the left-most key of the right child node.
        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        """Returns True if the node is full."""
        return len(self.keys) == self.order

    def show(self, counter=0):
        global result
        """Prints the keys at each level."""
        keys_at_each_level=self.keys
        print("*********************")
        result.append(keys_at_each_level)
        print("*********************")
        print(counter, str(self.keys))
        

        # Recursively print the key of child nodes (if these exist).
        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)

class BPlusTree(object):
    """B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split occurs, a key will
    'float' upwards and be inserted into the parent node to act as a pivot.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        """ For a given node and key, returns the index where the key should be inserted and the
        list of values at that index."""
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        """For a parent and child node, extract a pivot from the child to be inserted into the keys
        of the parent. Insert the values from the child into the values of the parent.
        """
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
        the leaf node into two.
        """
        parent = None
        child = self.root

        # Traverse tree until leaf node is reached.
        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        # If the leaf node is full, split the leaf node into two.
        if child.is_full():
            child.split()

            # Once a leaf node is split, it consists of a internal node and two leaf nodes. These
            # need to be re-inserted back into the tree.
            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def show(self):
        """Prints the keys at each level."""
        self.root.show()

def demo_bplustree():
    print('Initializing B+ tree...')
    bplustree = BPlusTree(order=6)
    f=open("i.csv","r")
    keys=[]
    
    print('Initializing node...')
    node = Node(order=3)
    lines=f.readlines()
    print(lines)
    for i in lines:
        k=i
        k=k.split('|')
        keys.append(int(k[0]))
    print(keys)
    
    for key in keys:
        for i in range(0,4):
            bplustree.insert(key,'a')
    bplustree.show()
        
    print("##############")

    






global i
global indsize 
indsize=0
i=[]
def iwrite(list_of_elem):
    global i
    global indsize
    with open('i.csv', 'w', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj,delimiter='\n')
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
def search_product(fusn):
    low=0
    high=len(i)-1
    while(low<=high):
        mid=(low+high)//2
        
        if(fusn==i[mid]):
            return mid
        elif(fusn>i[mid]):
            low = mid + 1
            
        else:
            high=mid-1
            
    return -1

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj,delimiter='|')
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def pack(pid,pname,pplace,price,pdelivery):
    rowcontents = [pid,pname,pplace,price,pdelivery]
    append_list_as_row('data.csv', rowcontents)

def unpack():
    
    i=0
    with open("data.csv") as file_name:
        file_read = csv.reader(file_name)
        
        array = file_read
        arrayOfProducts=[]
        
        for k in array:
            i=k
            for j in i:
                sub=j.split('|')
                arrayOfProducts.append(sub)
        return arrayOfProducts

app = Flask(__name__)
# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/view')
def index():
    array=unpack()
    return render_template('view.html',array=array)

@app.route('/display', methods=['GET', 'POST'])
def add_pup():
    global indsize
    if(request.method=='POST'):
        pname=request.form.get('pname')
        pplace=request.form.get('pplace')
        pid=request.form.get('pid')
        price=request.form.get('price')
        pdelivery=request.form.get('pdelivery')
        array=[pid,pname,pplace,price,pdelivery]
        if(search_product(int(pid))==-1):
            indsize=indsize+1
            i.append(int(pid))
            append_list_as_row('data.csv',array)
            i.sort()
            iwrite(i)
            
    
       
        print("############")
        print(pname+pplace+pid+price+pdelivery)
        print("############")
        array=unpack()
        return render_template('view.html',array=array)

    return render_template('display.html')
@app.route('/modify')
def modify():
    return render_template('modify.html')

@app.route('/search')
def search():
    
    return render_template('search.html')

@app.route('/list', methods=['GET', 'POST'])
def list():
    global result
   
    return render_template('list.html',result=result)

@app.route('/remove', methods=['GET', 'POST'])

def del_pup():
    global res
    res=""
    
    
    if(request.method=='POST'):
         pid=request.form.get('pid')
         ar=unpack()
         for order in ar:
            if(pid==order[0]):
                message="Order found"
                result=order
                return render_template('remove.html',message=message,result=result)
         message="Order not found"
         return render_template('remove.html',message=message)
        
        

         
      
        
            

   
    return render_template('remove.html')


if __name__ == '__main__':
    print('\n')
    demo_bplustree()
    app.run(debug=True)
