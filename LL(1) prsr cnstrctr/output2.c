Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
 RESTART: E:\Achint's\College\3rd Yr\LL(1) prsr cnstrctr\LL(1) prsr cnstrctr.py 
Enter the CFG, ^ can be used as Epsilon
Enter a Production(EOP)~S->aABb
Enter a Production(EOP)~A->aAc|^
Enter a Production(EOP)~B->bB|c
Enter a Production(EOP)~EOP

Terminals are {'a', 'c', 'b', '^'}
NonTerminals are {'S', 'B', 'A'}

Enter the Start Symbol~S
Press 0 to filter for useless symbols~0

Given Productions are
S -> {'aABb'}
A -> {'aAc', '^'}
B -> {'c', 'bB'}

Final Terminals are {'a', 'c', 'b', '^'}
Final NonTerminals are {'S', '#', 'B', 'A'}
Final Productions are
S -> {'aABb'}
A -> {'aAc', '^'}
B -> {'c', 'bB'}

*****First Sets*****
a {'a'}
S {'a'}
^ {'^'}
# {'a'}
c {'c'}
b {'b'}
B {'c', 'b'}
A {'a', '^'}

*****Follow Sets*****
S {'$'}
a {'a', 'c', 'b'}
# set()
c {'c', 'b'}
b {'c', 'b', '$'}
A {'c', 'b'}
B {'b'}

Enter a string to be parsed(NULL)~aacbbcb
		Given String Parsed Successfully

Enter a string to be parsed(NULL)~abc
ERROR! Terminal mismatch (TOS & next input)

Enter a string to be parsed(NULL)~acb
		Given String Parsed Successfully

Enter a string to be parsed(NULL)~abb
ERROR! No Entry in Parsing Table

Enter a string to be parsed(NULL)~NULL
Thanks for using LL(1) Parser Constructor
                -Achint Chaudhary
>>> 
