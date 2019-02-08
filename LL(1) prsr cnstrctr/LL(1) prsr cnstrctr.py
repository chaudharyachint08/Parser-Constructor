ReadMe='''This Program is a LL(1) parser constructor
It takes as input a given grammar
Automatically separates Terminals & Non-Terminals
Then it can(if asked) remove useless symbols from given grammar
Compute FIRST & FOLLOW sets for Non-Terminal symbols of grammar
Creates parsing table from it, check if grammar is fit for LL(1) parsing
Take any number of strings to be parsed, & return if they can be parsed
Reports appropriate errors if a string cannot be parsed
['#'] is initial stack configuration before parsing starts
$ is EOF(End-Of-File Marker)
# is Start symbol hidden from user with production\n #->Given start symbol
Ø ⇒ → α β γ δ ε ∅ ∈ ∗ ∴ ∵ ⊂ ⊃ ⊄ ⊅ ⊆ ⊇ ⊈ ⊉
'''

from copy import deepcopy

print('Enter the CFG, ^ can be used as Epsilon')

NonTerminals,AllSymbols=set(),set()

prod={}

while True:
    io=input('Enter a Production(EOP)~')
    if io=='EOP':#EOP is End of Productions
        break
    if io=='':
        continue
    AllSymbols.update(set(io).difference({'-','>','|'}))
    N,List=io.split('->')
    if N in prod:
        for i in List.split('|'):
            prod[N].add(i)
    else:
        prod[N]=set()
        NonTerminals.update(N)
        for i in List.split('|'):
            prod[N].add(i)

Terminals=AllSymbols.difference(NonTerminals)

print('\nTerminals are',Terminals)
print('NonTerminals are',NonTerminals)

NonTerminals.add('#')#Extra Start Symbol Added By Program

strt=input('\nEnter the Start Symbol~')
flag=input('Press 0 to filter for useless symbols~')
print('\nGiven Productions are')

for i in prod:
    print(i,'->',prod[i])

prod['#']={strt}

#Code for Removal of Useless Symbols

if flag=='0':
    
    N,T,P,S = NonTerminals,Terminals,prod,'#'

    # Test for αXβ ⇒∗ w , where w ∈ T*

    N_old=set()
    N_new=set(X for X in N if any(set(i)<=T for i in P[X]))

    while N_old!=N_new:
        N_old=deepcopy(N_new)
        N_new.update(set(X for X in N if any(set(i)<=(T|N_old) for i in P[X])))

    for i in N-N_old:
        del P[i]

    N=N_old


    # Test for  S ⇒∗ αXβ  , where X ∈ N

    N2,T2=set(S),set()

    while True:
        N_temp,T_temp=deepcopy(N2),deepcopy(T2)
        for i in N2:
            for j in P[i]:
                for k in set(j):
                    if k in N:
                        N_temp.add(k)
                    if k in T:
                        T_temp.add(k)
                        
        if N2==N_temp and T2==T_temp:
            break
        N2,T2=N_temp,T_temp
        
    N,T=N2,T2

    for i in P:
        for j in deepcopy(P[i]):
            if not set(j)<=(N|T):
                P[i].remove(j)

    uslss=set(P.keys())-N
    for i in uslss:
        del P[i]
    
    NonTerminals,Terminals=N,T
    AllSymbols = N|T
	
    print('\nFinal Terminals are',Terminals)
    print('Final NonTerminals are',NonTerminals)

    print('Final Productions are')

    for i in prod:
        if i=='#':continue
        print(i,'->',prod[i])
    
#FIRST & FOLLOW set computation for Parsing Table construction

first={}

def First_NonTrmnl_and_Trmnl():
    for a in Terminals:
        first[a]={a}
    first['^']={'^'}
    first['$']={'$'}
    for A in NonTerminals:
        first[A]=set()
    while True:
        old=deepcopy(first)
        for A in prod:
            for X in prod[A]:
                n=len(X)-1
                first[A].update(first[X[0]]-{'^'})
                i=0
                while ( ('^' in first[X[i]] ) and i<n ):
                    i+=1
                    first[A].update(
                        first[X[i]]-{'^'})
                if ( (i==n) and ('^' in first[X[n]]) ):
                    first[A].update({'^'})
        if first==old:
            break

def First(string):
    if string in first:
        return first[string]
    first[string]=set()
    n=len(string)-1
    first[string].update(first[string[0]]-{'^'})
    i=0
    while ( ('^' in first[string[i]] ) and i<n ):
        i+=1
        first[string].update(first[string[i]]-{'^'})
    if ( (i==n) and ('^' in first[string[n]]) ):
        first[string].update({'^'})
    return first[string]

follow={}

def Follow() :
    for X in AllSymbols.difference( {'^','#'} ) :
        follow[X] = set()
    follow[strt] = {'$'}
    while True :
        old = deepcopy(follow)
        for A in NonTerminals.difference( {'#'} ) :
            for X in prod[A] :
                if X == '^':
                    continue #RHS of production is NULL Production
                n = len(X) - 1
                follow[X[n]].update( follow[A] )
                rest = follow[A]
                for i in range(n,0,-1):
                    if '^' in first[X[i]]:
                        follow[X[i-1]].update(first[X[i]]-{'^'}|rest)
                    else:
                        follow[X[i-1]].update(first[X[i]])
                    rest=follow[X[i-1]]
                    
        if follow == old :
            break

First_NonTrmnl_and_Trmnl()

print('\n*****First Sets*****')
for i in first:
    print(i,first[i])
                                
Follow()
follow['#']=set()
print('\n*****Follow Sets*****')
for i in follow:
    print(i,follow[i])

#Parsing Table Contruction

PrsngTbl={}

for i in NonTerminals:
    PrsngTbl[i]={}
    for j in Terminals.union('$'):
        PrsngTbl[i][j]=set()

for A in prod:
    for i in prod[A]:
        for j in First(i):
            PrsngTbl[A][j].update({i})
        if '^' in First(i):
            for j in follow[A]:
                PrsngTbl[A][j].update({i})
            if '$' in follow[A]:
                PrsngTbl[A]['$'].update({i})

#To print Parsing Table

'''                
for i in PrsngTbl:
    for j in PrsngTbl[i]:
        print(i,j,PrsngTbl[i][j])
'''

try:
    for i in PrsngTbl:
        for j in PrsngTbl[i]:
            if j=='^':
                PrsngTbl[i][j]=''
                continue
            elif PrsngTbl[i][j]==set():
                PrsngTbl[i][j]=''
                continue
            elif len(PrsngTbl[i][j])>1:
                raise ZeroDivisionError('Multiple Entries in Parsing Table')
            PrsngTbl[i][j]=PrsngTbl[i][j].pop()

#Parser Constructed upto here, String are taken & checked if they can be parsed'

    while True:
        string=input('\nEnter a string to be parsed(NULL)~')
        if string=='NULL':
            print('Thanks for using LL(1) Parser Constructor\n\
                -Achint Chaudhary')
            break
        string+='$'
        stck=['#']#initial configuration of stack
        indx=0
        while True:
            X=stck[-1]
            sym=string[indx]
            if X in Terminals.union('$'):
                if X=='^':
                    stck.pop()
                    continue
                if X==sym:
                    stck.pop()
                    indx+=1
                else:
                    print("ERROR! Terminal mismatch (TOS & next input)")
                    break
            else:
                if PrsngTbl[X][sym]=='':
                    print('ERROR! No Entry in Parsing Table')
                    break
                else:
                    stck.pop()
                    stck.extend(list(reversed(PrsngTbl[X][sym])))
            if stck==[] and string[indx]=='$':
                print('\t\tGiven String Parsed Successfully')
                break
            if stck==[] and not string[indx]=='$':
                print('ERROR! Stack Emptied before $ occurs')
                break

except ZeroDivisionError as err:
    print('Grammar is not LL(1)',err)
