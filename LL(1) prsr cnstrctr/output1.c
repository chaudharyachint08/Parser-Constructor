Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
 RESTART: E:\Achint's\College\3rd Yr\LL(1) prsr cnstrctr\LL(1) prsr cnstrctr.py 
Enter the CFG, ^ can be used as Epsilon
Enter a Production(EOP)~S->aAS|c
Enter a Production(EOP)~A->ba|SB
Enter a Production(EOP)~B->bA|S
Enter a Production(EOP)~EOP

Terminals are {'b', 'c', 'a'}
NonTerminals are {'A', 'B', 'S'}

Enter the Start Symbol~S
Press 0 to filter for useless symbols~0

Given Productions are
A -> {'ba', 'SB'}
B -> {'bA', 'S'}
S -> {'c', 'aAS'}

Final Terminals are {'b', 'c', 'a'}
Final NonTerminals are {'A', 'B', 'S', '#'}
Final Productions are
A -> {'ba', 'SB'}
B -> {'bA', 'S'}
S -> {'c', 'aAS'}

*****First Sets*****
^ {'^'}
B {'c', 'b', 'a'}
b {'b'}
a {'a'}
A {'c', 'b', 'a'}
c {'c'}
S {'c', 'a'}
# {'c', 'a'}

*****Follow Sets*****
B {'c', 'a'}
b {'b', 'a', 'c'}
a {'b', 'a', 'c'}
A {'c', 'a'}
c {'b', 'a', 'c', '$'}
S {'b', 'a', 'c', '$'}
# set()

Enter a string to be parsed(NULL)~acbbac
		Given String Parsed Successfully

Enter a string to be parsed(NULL)~ac
ERROR! No Entry in Parsing Table

Enter a string to be parsed(NULL)~acbbacb
ERROR! Stack Emptied before $ occurs

Enter a string to be parsed(NULL)~NULL
Thanks for using LL(1) Parser Constructor
                -Achint Chaudhary
>>> 
