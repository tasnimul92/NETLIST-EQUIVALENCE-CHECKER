from EDA_Project import *
dir1 = 'I:\PythonCodes\EDA\netlists'  #give the desired directory for netlisists here
print('nets1' '=',nets1)
print('\n')
print('nets2' '=',nets2)
print('\n')
print("inputs1" '=' ,inputs1)
print('\n')
print("inputs2" '=' ,inputs2)
print('\n')
print("outputs1" '=' ,outputs1)
print('\n')
print("outputs2" '=' ,outputs2)
print('\n')
print("mapping1" '=' ,mapping1)
print('\n')
print("mapping2" '=' ,mapping2)
print('\n')
print("gates1 =")
print(gates1)
print('\n')
print("gates2 =")
print(gates2)
Cnfnetlist1=CreateCnf()
Cnfnetlist1.firstcnf(gates1,0) #creating part of the cnf from the first netlist
CnfnetlistSecond=CreateCnf()
CnfnetlistSecond.firstcnf(gates2,nets1) #creating part of the cnf from the second netlist and nets1 is sent to add with the literals
p=Cnfnetlist1.lateral
q=CnfnetlistSecond.lateral # in line 28 and 29 the two list of part of cnfs of two netlist are appended as one list
newoutput1={k: mapping1[k] for k in mapping1.keys() & set(outputs1)} #create a new dictionary for only the mapped values from output1 i.e newoutput1= {'f': 3}
newoutput2={l: mapping2[l] for l in mapping2.keys() & set(outputs2)}
meiter=CreateCnf()
meiter.metercircuit(newoutput1,newoutput2,nets1)
r=meiter.lateral

print('\n')
#print(p+q+r)
newinput1={ko: mapping1[ko] for ko in mapping1.keys() & set(inputs1)} #create a new dictionary for only the mapped values from inpput1
newinput2={lo: mapping2[lo] for lo in mapping2.keys() & set(inputs2)}
equi=CreateCnf()
#print('equi')
equi.equivalent(newinput1,newinput2,nets1)
so=equi.lateral
print('CNF')
print(so)
print('\n')
Devis=DavisPutnam()
Devis.DevPut(so,0)


