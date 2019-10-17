
all: c4

c4:	ConnectFour.o main.o MCTS.o
	g++ -Wall -std=c++11 -o c4 ConnectFour.o main.o MCTS.o

main.o:	main.cpp ConnectFour.h MCTS.h
	g++ -c main.cpp

MCTS.o: MCTS.cpp MCTS.h
	g++ -c MCTS.cpp

ConnectFour.o:	ConnectFour.cpp ConnectFour.h
	g++ -c ConnectFour.cpp


clean:	
	rm -f c4 *.o

