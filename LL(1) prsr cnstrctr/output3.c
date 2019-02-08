Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
 RESTART: E:\Achint's\College\3rd Yr\LL(1) prsr cnstrctr\LL(1) prsr cnstrctr.py 
Enter the CFG, ^ can be used as Epsilon
Enter a Production(EOP)~S->AB|CA
Enter a Production(EOP)~A->a
Enter a Production(EOP)~B->BC|AB
Enter a Production(EOP)~C->aB|b
Enter a Production(EOP)~D->d
Enter a Production(EOP)~EOP

Terminals are {'a', 'b', 'd'}
NonTerminals are {'C', 'D', 'B', 'A', 'S'}

Enter the Start Symbol~S
Press 0 to filter for useless symbols~0

Given Productions are
C -> {'aB', 'b'}
D -> {'d'}
A -> {'a'}
S -> {'AB', 'CA'}
B -> {'AB', 'BC'}

Final Terminals are {'a', 'b'}
Final NonTerminals are {'C', 'A', 'S', '#'}
Final Productions are
A -> {'a'}
S -> {'CA'}
C -> {'b'}

*****First Sets*****
^ {'^'}
A {'a'}
S {'b'}
a {'a'}
C {'b'}
# {'b'}
b {'b'}

*****Follow Sets*****
A {'$'}
S {'$'}
a {'$'}
C {'a'}
# set()
b {'a'}

Enter a string to be parsed(NULL)~ba
		Given String Parsed Successfully

Enter a string to be parsed(NULL)~NULL
Thanks for using LL(1) Parser Constructor
                -Achint Chaudhary
>>>
>>>'ba' is the only Derivable string
