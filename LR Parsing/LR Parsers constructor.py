ReadMe='''This Program is a all  LR parsers constructor
It takes as input a given grammar
Automatically separates Terminals & Non-Terminals
Then it can(if asked) remove useless symbols from given grammar
Compute FIRST & FOLLOW sets for Non-Terminal symbols of grammar

Ask user to create type of Parsing Table
1. SLR(1)
2. CLR(1)
3. LALR(1)
4. ILR(1)

Creates parsing table from it, check if grammar is fit for that parsing
Take any number of strings to be parsed, & return if they can be parsed
Reports appropriate errors if a string cannot be parsed
$ is EOF(End-Of-File Marker)
# is Start symbol hidden from user with production\n #->Given start symbol
This is the rule for augmented grammar
Ø ⇒ → α β γ δ ε ∅ ∈ ∗ ∴ ∵ ⊂ ⊃ ⊄ ⊅ ⊆ ⊇ ⊈ ⊉

be AWARE!! about DATA-STRUCTURES

'''

from copy import deepcopy

print('Enter the CFG, ^ can be used as Epsilon')

NonTerminals , AllSymbols = set() , set()

prod = {}   #'dictonary' type

while True:
    'This loop takes Input of prouctions from user'
    io = input('Enter a Production(EOP)~')
    if io == 'EOP' :    #EOP is End of Productions
        break
    if io == '' :
        continue
    
    AllSymbols.update( set(io).difference( {'-','>','|'} ) )
    N , List = io.split('->')
    
    if N in prod:   #is that Non-Terminal is already as a entry in Productions
        for i in List.split('|') :
            if i not in prod[N] :
                prod[N].append(i)
    else:   # else create an entry for new Non-Terminal
        prod[N] = []
        NonTerminals.update(N)
        for i in List.split('|') :
            if i not in prod[N] :
                prod[N].append(i)


Terminals = AllSymbols.difference( NonTerminals )

print('\nTerminals are' , Terminals)
print('NonTerminals are' , NonTerminals)

NonTerminals.add('#')   #for Augmented Grammar Generation

strt = input('\nEnter the Start Symbol~')
flag = input('Press 0 to filter for useless symbols~')
print('\nGiven Productions are')

for i in prod:
    print( i , '->' , prod[i] )

prod['#'] = [strt]

#Code for Removal of Useless Symbols

if flag == '0' :
    
    N , T , P , S = NonTerminals , Terminals , prod , '#'

    # Test for αXβ ⇒∗ w , where w ∈ T*

    N_old = set()
    N_new = set(X for X in N if any(set(i)<=T for i in P[X]))

    while N_old != N_new :
        N_old = deepcopy(N_new)
        N_new.update( set(X for X in N if any(set(i)<=(T|N_old) for i in P[X])) )

    for i in N-N_old :
        del P[i]

    N = N_old


    # Test for  S ⇒∗ αXβ  , where X ∈ N

    N2 , T2 = set(S) , set()

    while True:
        N_temp , T_temp = deepcopy(N2) , deepcopy(T2)
        for i in N2 :
            for j in P[i] :
                for k in set(j) :
                    if k in N :
                        N_temp.add(k)
                    if k in T :
                        T_temp.add(k)
                        
        if N2 == N_temp and T2 == T_temp :
            break
        N2 , T2 = N_temp , T_temp
        
    N , T = N2 , T2

    for i in P :
        for j in deepcopy(P[i]) :
            if not set(j)<=(N|T) :
                P[i].remove(j)

    uslss = set(P.keys()) - N
    for i in uslss :
        del P[i]
    
    NonTerminals , Terminals = N , T
    AllSymbols = NonTerminals.union(Terminals)
	
    print('\nFinal Terminals are' , Terminals)
    print('Final NonTerminals are' , NonTerminals)

    print('Final Productions are')

    for i in prod :
        if i == '#' :
            continue
        print( i , '->' , prod[i] )
    
#FIRST & FOLLOW set computation for Parsing Table construction

first = {}

def First_NonTrmnl_and_Trmnl() :
    for a in Terminals :
        first[a] = {a}
    first['^'] = {'^'}
    first['$'] = {'$'}
    for A in NonTerminals :
        first[A] = set()
    while True :
        old = deepcopy(first)
        for A in prod :
            for X in prod[A] :
                n = len(X) - 1
                first[A].update( first[X[0]] - {'^'} )
                i = 0
                while ( ('^' in first[X[i]] ) and i < n ) :
                    i += 1
                    first[A].update( first[X[i]] - {'^'} )
                if ( (i == n) and ('^' in first[X[n]]) ) :
                    first[A].update( {'^'} )
        if first == old :
            break

def First(string) :
    if string in first :
        return first[string]
    first[string] = set()
    n = len(string) - 1
    first[string].update( first[string[0]] - {'^'} )
    i = 0
    while ( ('^' in first[string[i]] ) and i < n ) :
        i += 1
        first[string].update( first[string[i]] - {'^'} )
    if ( (i == n) and ('^' in first[string[n]]) ) :
        first[string].update( {'^'} )
    return first[string]

follow = {}

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
for i in first :
    print( i , first[i] )
                                
Follow()

follow['#'] = set()

print('\n*****Follow Sets*****')
for i in follow :
    print( i , follow[i] )

#both Kernel_Items & Non_Kernel_Items are of type SET here\
#but for memory optimization, it must be dict type, set chosen only for convenience

Kernel_Items = { ( '#' , '.'+strt ) }

Non_Kernel_Items = set()

for i in prod :
    for j in prod[i] :
        if j == '^' :
            prod[i].remove( '^' )
            prod[i].append( '' )
            j=''
        Non_Kernel_Items.add( ( i , '.'+j ) )

Non_Kernel_Items.remove( ( '#' , '.'+strt ) )

for i in prod :
    for j in prod[i] :
        for k in range(len(j)):
            Kernel_Items.add( ( i , j[:k+1]+'.'+j[k+1:] ) )


print('Kernel_Items')
for i in Kernel_Items :
    print( i )

print('Non_Kernel_Items')
for i in Non_Kernel_Items :
    print( i )

#Terminals & NonTermiansl sets are convertd to list, for deterministic ordering
Terminals    = list(  Terminals.union( {'$'} )    )
NonTerminals = list(  NonTerminals.difference( {'#'} ) )

AllSymbls = Terminals + NonTerminals

DFA = {}    #Storage of Items of a state in form of list
'''
LR(0) , LR(1) or ILR(1) automaton will be created in this DFA dictionary
KEY denotes the state_number
VALUE denotes a set of Items in that state(can be Krnl or Non-Krnl items)
specs of VALUE depends on whether user asked for LR(0) or LR(1)( or ILR(1) ) automaton
'''

TrnstnTbl = {}  #TransitionTable of above DFA, helps in building Parsing Table
'''
This Transition Table contains the moves made by DFA on each symbol, which means
each entry is a LIST with same order as that in LIST AllSymbls
LIST initialized by all -1(an invalid/ERROR! state)
'''
PrsngTbl = {}   #Parsing Table itself
'''
Each entry of parsing table is a list of set
to which shift or reduce moves can be added
conflicts are reported later on, to user, & can be eliminated also
there is no distinction for ACTION & GOTO part in storage
Program discriminates using LIST AllSymbls
'''
#Each of above 3 DataStructures has keys as state number of DFA


print('Select Type of Parser to be costructed')
choice=input(' 1. SLR(1)\n 2. CLR(1)\n 3. LALR(1)\n 4. ILR(1) ~')

def Resolve():
    pass

def closure0 ( I ) :
    while True:
        J=deepcopy(I)
        for i in J:
            if i[1].index('.')+1!=len(i[1]):
                sym=i[1][i[1].index('.')+1]
                if sym in NonTerminals:
                    for j in Non_Kernel_Items:
                        if j[0]==sym:
                            I.add(j)
        if I==J:
            break
        
    return I #as I==J here, J can also be returned

def goto0 ( I , X ) :
    valid=set()
    for i in I:
        if i[1].index('.')+1!=len(i[1]):
            sym=i[1][i[1].index('.')+1]
            if sym==X:
                valid.add( (i[0],i[1].replace('.'+X,X+'.')) )

    return closure0(valid)

def SLR () :
    
    #State & Transition Table Construction
    indx = 0
    
    DFA[indx] = closure0( { ('#' , '.'+strt) } )
    TrnstnTbl[indx] = [' ']*len(AllSymbls)
    
    queue = [indx]

    while queue != [] :
        crrnt_state = queue.pop( 0 )
        for X in AllSymbls :
            nxt = goto0( DFA[crrnt_state] , X )
            if nxt != set():
                for i in range(indx+1):
                    if DFA[i]==nxt:
                        TrnstnTbl[crrnt_state][AllSymbls.index(X)] = i
                        break
                else:
                    indx += 1
                    DFA[indx] = nxt
                    TrnstnTbl[indx] = [' ']*len(AllSymbls)
                    TrnstnTbl[crrnt_state][AllSymbls.index(X)] = indx
                    queue.append(indx)

    #Parsing Table Construction

    #Part-1 Shift Actions & GOTO Part of Parsing Table
    
    for i in range(indx+1):
        #[set()]*len(AllSymbls) This Gives Error
        PrsngTbl[i]=[set() for j in range(len(AllSymbls))]
        for j in range(len(AllSymbls)):
            nxt=TrnstnTbl[i][j]
            if nxt!=' ':
                if j<len(Terminals):
                    PrsngTbl[i][j].add(('S',nxt))
                else:
                    PrsngTbl[i][j].add(nxt)

    
    #Part-2 Reduce Actions of Parsing Table
    for i in range(indx+1):
        for j in DFA[i]:
            if j[1].index('.')+1 == len(j[1]):
                for k in follow[j[0]]:
                    PrsngTbl[i][AllSymbls.index(k)].add( ('R' , (j[0] , j[1][:-1]) ) )

    for i in range(indx+1):
        for j in range(len(AllSymbls)):
            if PrsngTbl[i][j]==set():
                PrsngTbl[i][j]='ERR'
            elif len(PrsngTbl[i][j])==1:
                PrsngTbl[i][j]=PrsngTbl[i][j].pop()
            else:
                print('Multiple Entries in SLR Parsing Table',i,j)
                Resolve()

    for i in range(indx+1):
        if ('#',strt+'.') in DFA[i]:
            PrsngTbl[i][AllSymbls.index('$')]='ACC'
    

def closure1 ( I ) :
    while True:
        J=deepcopy(I)
        for i in J:
            if i[1].index('.')+1!=len(i[1]):
                val=i[1].index('.')+1
                sym=i[1][val]
                if sym in NonTerminals:
                    for j in Non_Kernel_Items:
                        if j[0]==sym:
                            for k in First(i[1][val+1:]+i[2]):
                                I.add(j+(k,))
        if I==J:
            break
        
    return I #as I==J here, J can also be returned

def goto1 ( I , X ) :
    valid=set()
    for i in I:
        if i[1].index('.')+1!=len(i[1]):
            sym=i[1][i[1].index('.')+1]
            if sym==X:
                valid.add( ( i[0] , i[1].replace('.'+X,X+'.') , i[2] ) )

    return closure1(valid)

def CLR () :
    
    #State & Transition Table Construction
    indx = 0
    
    DFA[indx] = closure1( { ('#' , '.'+strt , '$') } )
    TrnstnTbl[indx] = [' ']*len(AllSymbls)
    
    queue = [indx]

    while queue != [] :
        crrnt_state = queue.pop( 0 )
        for X in AllSymbls :
            nxt = goto1( DFA[crrnt_state] , X )
            if nxt != set():
                for i in range(indx+1):
                    if DFA[i]==nxt:
                        TrnstnTbl[crrnt_state][AllSymbls.index(X)] = i
                        break
                else:
                    indx += 1
                    DFA[indx] = nxt
                    TrnstnTbl[indx] = [' ']*len(AllSymbls)
                    TrnstnTbl[crrnt_state][AllSymbls.index(X)] = indx
                    queue.append(indx)

    #Parsing Table Construction

    #Part-1 Shift Actions & GOTO Part of Parsing Table
    
    for i in range(indx+1):
        #[set()]*len(AllSymbls) This Gives Error
        PrsngTbl[i]=[set() for j in range(len(AllSymbls))]
        for j in range(len(AllSymbls)):
            nxt=TrnstnTbl[i][j]
            if nxt!=' ':
                if j<len(Terminals):
                    PrsngTbl[i][j].add(('S',nxt))
                else:
                    PrsngTbl[i][j].add(nxt)

    
    #Part-2 Reduce Actions of Parsing Table
    for i in range(indx+1):
        for j in DFA[i]:
            if j[1].index('.')+1 == len(j[1]):
                PrsngTbl[i][AllSymbls.index(j[2])].add( ('R' , (j[0] , j[1][:-1]) ) )

    for i in range(indx+1):
        for j in range(len(AllSymbls)):
            if PrsngTbl[i][j]==set():
                PrsngTbl[i][j]='ERR'
            elif len(PrsngTbl[i][j])==1:
                PrsngTbl[i][j]=PrsngTbl[i][j].pop()
            else:
                print('Multiple Entries in CLR Parsing Table',i,j)
                Resolve()

    for i in range(indx+1):
        if ('#',strt+'.','$') in DFA[i]:
            PrsngTbl[i][AllSymbls.index('$')]='ACC'
    

def match_core ( i , j ) :
    set1 , set2 = set() , set()
    for k in DFA[i]:
        set1.add( (k[0],k[1]) )
    for k in DFA[j]:
        set2.add( (k[0],k[1]) )

    if set1 == set2:
        return 1
    return 0


def LALR() :
    CLR()   #Easier but not Efficient Algorithm of LALR Parser Construction
    rmvd = set()
    while True:
        flag = 0
        for i in DFA:
            if i in rmvd:
                continue
            merger = { i }
            for j in DFA :
                if j in rmvd:
                    continue
                if match_core(i,j) :
                    merger.add(j)
                    
            if len(merger) > 1 :
                #print('MergerSet=',merger,'Removed States',rmvd)
                flag = 1
                mstr = min(merger)
                for j in PrsngTbl:
                    for k in range(len(AllSymbls)) :
                        if k < len(Terminals) :
                            if PrsngTbl[j][k][0] == 'S' :
                                if PrsngTbl[j][k][1] in merger :
                                    PrsngTbl[j][k] = ('S',mstr)
                        else:
                            if PrsngTbl[j][k] in merger:
                                    PrsngTbl[j][k] = mstr

                RR_actions = {}
                for j in range(len(Terminals)):
                    RR_actions[AllSymbls[j]]=set()
                for j in merger:
                    for k in range(len(Terminals)):
                        # LALR can introduce R/R Conflicts only, S/R are from CLR
                        if PrsngTbl[j][k][0] == 'R' :
                            if AllSymbls[k] in RR_actions:
                                RR_actions[AllSymbls[k]].add( PrsngTbl[j][k][1] )

                    if j!=mstr:
                        del PrsngTbl[j]
                        del TrnstnTbl[j]
                        rmvd.add(j)

                for j in range(len(Terminals)):
                    if len(RR_actions[AllSymbls[j]]) == 1 :
                        PrsngTbl[mstr][j] = ('R' , RR_actions[AllSymbls[j]].pop())
                    elif len(RR_actions[AllSymbls[j]])>1:
                        print('R/R Conflicts Generated due merging',merger,AllSymbls[j])
                        print( RR_actions[AllSymbls[j]] )
                    
        if flag==0:
            print('CLR in ',len(DFA),'states, by LALR in',len(PrsngTbl),'states')
            break

def rr_conflicts ( merger ):
    complete = set()
    for i in merger:
        complete.update(DFA[i])

    hsh={}
    for N,P,T in complete:
        if (P,T) in hsh:
            hsh[(P,T)].add(N)
        else:
            hsh[(P,T)] = set()
            hsh[(P,T)].add(N)

    for i in hsh:
        if len(hsh[i])>1:
            return 1
        
    return 0

def ILR () :
    CLR()   #Easier but not Efficient Algorithm of ILR Parser Construction
    rmvd = set()
    while True:
        flag = 0
        for i in DFA:
            if i in rmvd:
                continue
            merger = { i }
            for j in DFA :
                if j in rmvd:
                    continue
                if match_core(i,j) and not rr_conflicts(merger|{j}):
                    merger.add(j)
                    
            if len(merger) > 1 :
                #print('MergerSet=',merger,'Removed States',rmvd)
                flag = 1
                mstr = min(merger)
                for j in PrsngTbl:
                    for k in range(len(AllSymbls)) :
                        if k < len(Terminals) :
                            if PrsngTbl[j][k][0] == 'S' :
                                if PrsngTbl[j][k][1] in merger :
                                    PrsngTbl[j][k] = ('S',mstr)
                        else:
                            if PrsngTbl[j][k] in merger:
                                    PrsngTbl[j][k] = mstr

                RR_actions = {}
                for j in range(len(Terminals)):
                    RR_actions[AllSymbls[j]]=set()
                for j in merger:
                    for k in range(len(Terminals)):
                        # LALR can introduce R/R Conflicts only, S/R are from CLR
                        if PrsngTbl[j][k][0] == 'R' :
                            if AllSymbls[k] in RR_actions:
                                RR_actions[AllSymbls[k]].add( PrsngTbl[j][k][1] )

                    if j!=mstr:
                        del PrsngTbl[j]
                        del TrnstnTbl[j]
                        rmvd.add(j)

                for j in range(len(Terminals)):
                    if len(RR_actions[AllSymbls[j]]) == 1 :
                        PrsngTbl[mstr][j] = ('R' , RR_actions[AllSymbls[j]].pop())
                    elif len(RR_actions[AllSymbls[j]])>1:
                        print('R/R Conflicts Generated due merging',merger,AllSymbls[j])
                        print( RR_actions[AllSymbls[j]] )
                    
        if flag==0:
            print('CLR in ',len(DFA),'states, by IALR in',len(PrsngTbl),'states')
            break


if   choice == '1' :
    SLR()
elif choice == '2' :
    CLR()
elif choice == '3' :
    LALR()
elif choice == '4' :
    ILR()
else:
    print('Invalid Choice of Parser Type')

try:
    if int(choice) in (1,2,3,4):
        while True:
            ip = input('Enter a String to be Parsed~')+'$'
            stck = [0]
            indx = 0
            try:
                while True:
                    print(stck,'   ',ip[indx:])
                    val=PrsngTbl[stck[-1]][AllSymbls.index(ip[indx])]
                    if val=='ACC':
                        print('\t\tString Parsed Successfully.... :) :)')
                        break
                    elif val=='ERR':
                        print('\t\tString Cannot be Parsed.... :( :(')
                        break
                    elif val[0]=='S':
                        stck.append(val[1])
                        indx+=1
                    elif val[0]=='R':
                        if len(val[1][1])!=0:
                            stck=stck[:-1*len(val[1][1])]
                        stck.append( PrsngTbl[stck[-1]][AllSymbls.index(val[1][0])] )
            except:
                print('\t\tUnexpected Error.... !!')
                #PrsngTbl is used to Parse Any Number of Strings
except:
    print('Thanks for using LR Parser Construction tool\n\t-Achint Chaudhary')
