
import copy
from tkinter import *
from tkinter.filedialog import askopenfilename
root = Tk()  # for tkinter
#root.destroy()
root1 = Tk()
#root1.destroy()
ftypes = [('net file', "*.net")]
ttl = "Choose files"
dir1=''

def readNetlist(file):
    nets = int(file.readline())  # reads a single line from the file
    inputs = file.readline().split()  # split strings with blankspace or white space
    inputs.sort()  # default sorting with numbers then letters
    outputs = file.readline().split()
    outputs.sort()

    # read mapping
    mapping = {}  # empty list or dictionary
    while True:
        line = file.readline().strip()  # remove white space from all the strings line by line that is in the beginning and the end
        if not line:
            break

        net, name = line.split()  # split
        mapping[name] = int(net)

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        ports = map(int, bits)
        gates.append((gate, [int(x) for x in ports]))  # here gates is appended as a dictionary as ('and', [1, 2, 3])

    return inputs, outputs, mapping, gates, nets

class CreateCnf:
    lateral = []
    def firstcnf(self, Gates, binary):
     self.binary = binary
     self.Gates=Gates
     for values in Gates:
         value = values[1] #creating a list with clause
         value=[f+binary for f in value]  # here literals of the clause are added with certain values for creating the cnf perfectly
         if values[0] == 'and':
             x = (value[0], -value[2])
             self.lateral.append(x)
             y = (value[1], -value[2])
             self.lateral.append(y)
             z = (-value[0], -value[1], value[2])
             self.lateral.append(z)

         elif values[0] == 'or':
             x = (-value[0], value[2])
             self.lateral.append(x)
             y = (-value[1], value[2])
             self.lateral.append(y)
             z = (value[0], value[1], -value[2])
             self.lateral.append(z)

         elif values[0] == 'inv':
             x = (value[0], value[1])
             self.lateral.append(x)
             y = (-value[0], -value[1])
             self.lateral.append(y)

         elif values[0] == 'xor':
             x = (value[0], value[1], -value[2])
             self.lateral.append(x)
             y = (-value[0], -value[1], -value[2])
             self.lateral.append(y)
             z = (value[0], -value[1], value[2])
             self.lateral.append(z)
             o=(-value[0], value[1], value[2])
             self.lateral.append(o)
         else:
             print('null') #its useless


    def metercircuit(self, Newouput1,Newouput2,binary):
        self.new1=Newouput1
        self.new2=Newouput2
        g=set(Newouput1)  #its just necessary to  use dictionary properly in the for loop of line 93
        h=set(Newouput2)
        for k in Newouput2.keys():
            Newouput2[k] += binary  #just for adding particular value to each literals
        liste=[1]
        inc = nets1+nets2
        lis=()
        for ke in g.intersection(h): #comparing keys of two dictionaries
              if len(ke)/3 == 1:
                 vujung=1
              else:
                  vujung=1
              inc=inc+vujung
              liste.append(inc)
# xor for comparing outputs
              x=(Newouput1[ke],Newouput2[ke],-inc)
              self.lateral.append(x)
              y=(-Newouput1[ke],-Newouput2[ke],-inc)
              self.lateral.append(y)
              z = (-Newouput1[ke], Newouput2[ke], inc)
              self.lateral.append(z)
              o=(Newouput1[ke], -Newouput2[ke], inc)
              self.lateral.append(o)


        liste.pop(0)
        lis=liste
        self.lateral.append(lis)


    def equivalent(self, Newinput1,Newinput2,binary):
        self.neu1=Newinput1
        self.neu2 = Newinput2
        go=set(Newinput1)
        ho=set(Newinput2)
        for k in Newinput1.keys():
            Newinput2[k] += binary
        for kel in go.intersection(ho):
            xo=(-Newinput1[kel], Newinput2[kel])
            self.lateral.append(xo)
            yo = (Newinput1[kel], -Newinput2[kel])
            self.lateral.append(yo)


class DavisPutnam:
    literallist = []

    def counterExample(self,survivedliterallist):
        print("Printing Counter Example")
        self.survivedliterallist = survivedliterallist
        survivedliterallist=list(set(survivedliterallist))
        print(survivedliterallist)
        print("Inputs : ")
        for x in range(0, len(survivedliterallist), 1):
               for key, value in mapping1.items():
                   if (key in inputs1) and (value == abs(survivedliterallist[x])):
                     if survivedliterallist[x]>0:
                              #print(survivedliterallist[x])
                        print(key, '= 1')
                     elif survivedliterallist[x]<0:
                        print(key, '= 0')
        print("Outputs1: ")
        for x in range(0, len(survivedliterallist), 1):
            #if abs(survivedliterallist[x]) < (nets1 + nets2):
                for key, value in mapping1.items():
                    if (key in outputs1) and (value == abs(survivedliterallist[x])):
                        if survivedliterallist[x] > 0:
                        # print(survivedliterallist[x])
                            print(key, '= 1')
                        elif survivedliterallist[x] < 0:
                            print(key, '= 0')
        print("Outputs2: ")
        for x in range(0, len(survivedliterallist), 1):
                for key, value in mapping2.items():
                    q = value + nets1
                    if (key in outputs2) and (q == abs(survivedliterallist[x])):
                        if survivedliterallist[x] > 0:

                            print(key, '= 1')
                        elif survivedliterallist[x] < 0:
                            print(key, '= 0')






    def DelRule(self, cnf,in_item):
        self.cnf=cnf
        self.in_item=in_item
        cnf = [tuple(filter(lambda x: x != -in_item, i)) for i in cnf]
        for u in range(0, len(cnf), 1):
            for k in cnf:
                if k.count(in_item):
                    cnf.remove(k)

        #print('delcnf')
        #print(cnf)
        return cnf

    def DevPut(self, createdcnf,lateral):
       self.createdcnf=createdcnf
       self.lateral=lateral

       #print(createdcnf)
       #print(len(createdcnf))
       if lateral !=0:
            createdcnf=self.DelRule(createdcnf,lateral)
       for unitclause in range(0,len(createdcnf),1):
             for clause in createdcnf:
                     if len(clause) ==1 :
                         #print('u')
                         newliteral=clause[0]
                         self.literallist.append(newliteral)
                         #print(newliteral)
                         #print(len(createdcnf))
                         createdcnf=self.DelRule(createdcnf,newliteral)

       if len(createdcnf)==0:
            print('soultion found')
            print('not equivalent')
            #self.CounterExample(self.literallist)
            self.counterExample(self.literallist)

            exit()
       for clause in range(0, len(createdcnf), 1):
           if len(createdcnf[clause]) == 0:
               print('no soultion')
               print('equivalent')
               exit()
               print(createdcnf)
               return

       #print(createdcnf)
       #print(len(createdcnf))
       deep_copy = copy.deepcopy(createdcnf)
       firstlateral = abs(createdcnf[-1][-1])
       #print(firstlateral)
       createdcnf = self.DelRule(createdcnf, -firstlateral)
       self.DevPut(createdcnf, -firstlateral)
       deep_copy = self.DelRule(deep_copy, firstlateral)
       self.DevPut(deep_copy, firstlateral)



root.fileName = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
root1.fileName = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
if root.fileName == "" or root1.fileName == "":
    print("Please select both netlist1 and netlist2")
    sys.exit()
else:
    inputs1, outputs1, mapping1, gates1, nets1 = readNetlist(open(root.fileName,"r"))  # represents the first command-line argument (as a string) supplied to the script in question. It will not prompt for input, but it will fail with an IndexError if no arguments are supplied on the command-line following the script name.
    inputs2,outputs2,mapping2,gates2,nets2 = readNetlist(open(root1.fileName,"r"))
