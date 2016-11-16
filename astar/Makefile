puzzle : q1.o q2.o q3.o q4.o aStar.o
	g++ -Wall q1.o aStar.o -o q1
	g++ -Wall q2.o aStar.o -o q2
	g++ -Wall q3.o aStar.o -o q3
	g++ -Wall q4.o aStar.o -o q4

aStar.o : aStar.h aStar.cpp
	g++ -Wall -c aStar.cpp

q1.o : q1.cpp
	g++ -Wall -c q1.cpp

q2.o : q2.cpp
	g++ -Wall -c q2.cpp

q3.o : q3.cpp
	g++ -Wall -c q3.cpp

q4.o : q4.cpp
	g++ -Wall -c q4.cpp
clean :
	\rm *.o q1 q2 q3
