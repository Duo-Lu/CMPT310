
#include "ConnectFour.h"
#include <iostream>
#include <stdlib.h>
// Desc:  Constructor
//  	  board : [5,0][5,1][5,2][5,3][5,4][5,5][5,6]
//				  [4,0][4,1][4,2][4,3][4,4][4,5][4,6]
//				  [3,0][3,1][3,2][3,3][3,4][3,5][3,6]
//				  [2,0][2,1][2,2][2,3][2,4][2,5][2,6]
//				  [1,0][1,1][1,2][1,3][1,4][1,5][1,6]
//				  [0,0][0,1][0,2][0,3][0,4][0,5][0,6]
ConnectFour::ConnectFour(){
	board = new char*[6];
	for(int i = 0; i < 6; i++){
		board[i] = new char[7];
	}
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 7; j++){
			board[i][j] = '+';
		}
	}

	// weightBoard = new double*[6];
	// for(int i = 0; i < 6; i++){
	// 	weightBoard[i] = new double[7];
	// }
	// for(int i = 0; i < 6; i++){
	// 	for(int j = 0; j < 7; j++){
	// 		weightBoard[i][j] = 0.0;
	// 	}
	// }

	heights = new int [7];
	for(int i = 0; i < 7; i++){
		heights[i] = 0;
	}
	// myPlayer = 'X';
	// myOpponent = 'O';
	curr_player = 'X';
	last_x = -2;
	last_y = -2;
	nAvailable = 7;
	nLeft = 42;
}

// Desc:  Copy constructor
ConnectFour::ConnectFour(const ConnectFour &rhs){
	board = new char*[6];
	for(int i = 0; i < 6; i++){
		board[i] = new char[7];
	}
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 7; j++){
			board[i][j] = rhs.board[i][j];
		}
	}

	// weightBoard = new double*[6];
	// for(int i = 0; i < 6; i++){
	// 	weightBoard[i] = new double[7];
	// }
	// for(int i = 0; i < 6; i++){
	// 	for(int j = 0; j < 7; j++){
	// 		weightBoard[i][j] = rhs.weightBoard[i][j];
	// 	}
	// }

	heights = new int [7];
	for(int i = 0; i < 7; i++){
		heights[i] = rhs.heights[i];
	}
	// myPlayer = rhs.myPlayer;
	// myOpponent = rhs.myOpponent;
	curr_player = rhs.curr_player;
	last_x = rhs.last_x;
	last_y = rhs.last_y;
	nAvailable = rhs.nAvailable;
	nLeft = rhs.nLeft;
}

// Desc:  Destructor
ConnectFour::~ConnectFour(){
	for(int i = 0; i < 6; i++){
		delete[] board[i];
	}
	delete[] board;
	//delete weightBoard;
	delete[] heights;
}

// Desc:  Set current player
void ConnectFour::setPlayer(char player){
	curr_player = player;
}

// Desc:  Get coordinate x of last move
int ConnectFour::getLastX(){
	return last_x;
}

// Desc:  Get coordinate y of last move
int ConnectFour::getLastY(){
	return last_y;
}

// Desc:  Get number of available moves
int ConnectFour::getN_Availables(){
	return nAvailable;
}

// Desc:  Get heights of columns
int* ConnectFour::getHeights(){
	return heights;
}

// Desc: Get game board
char** ConnectFour::getBoard(){
  return board;
}

// Desc:  Get number of empty entries
int ConnectFour::getN_Left(){
	return nLeft;
}

// Desc:  Make a move at column y(y in [0,6]) of player
//		  Return x coordinate
int ConnectFour::makeMove(int y, char player){
	curr_player = player;
	if(isAvailable(y)){
		last_y = y;
		int i;
		for(i = 0; i < 6; i++){
			if(board[i][y] == '+'){
				board[i][y] = player;
				break;
			}
		}
		last_x = i;
		heights[y] ++;
		nLeft --;

		//updateWeight(curr_player);

		curr_player = 'X'+'O' - curr_player;
		if(heights[y] == 6 && i == 5){
			nAvailable --;
		}
		return i;
	}
	return -2;//illegal move 
}

// Desc:  Make a move at column y(y in [0,6]) of player, does not update weights (used for AI playouts)
//		  Return x coordinate
// int ConnectFour::makeMove_unweight(int y, char player){
// 	curr_player = player;
// 	if(isAvailable(y)){
// 		last_y = y;
// 		int i;
// 		for(i = 0; i < 6; i++){
// 			if(board[i][y] == '+'){
// 				board[i][y] = player;
// 				break;
// 			}
// 		}
// 		last_x = i;
// 		heights[y] ++;
// 		nLeft --;

// 		//updateWeight(curr_player);

// 		curr_player = 'X'+'O' - curr_player;
// 		if(heights[y] == 6 && i == 5){
// 			nAvailable --;
// 		}
// 		return i;
// 	}
// 	return -2;//illegal move 
// }

// Desc: Update weight board, according to last x, y
//  	  board : [5,0][5,1][5,2][5,3][5,4][5,5][5,6]
//				  [4,0][4,1][4,2][4,3][4,4][4,5][4,6]
//				  [3,0][3,1][3,2][3,3][3,4][3,5][3,6]
//				  [2,0][2,1][2,2][2,3][2,4][2,5][2,6]
//				  [1,0][1,1][1,2][1,3][1,4][1,5][1,6]
//				  [0,0][0,1][0,2][0,3][0,4][0,5][0,6]
// void ConnectFour::updateWeight(char myPlayer){
// 	char myOpponent = 'X'+'O' - myPlayer;
// 	int ctr = 0;
// 	int beadCtr = 0;
	
// 	//vertical:
// 	for(int i = 1; i <= 3 && last_x-i >= 0 && board[last_x-i][last_y] != myOpponent; i++){
// 		char c = board[last_x-i][last_y];
// 		ctr += (c == myPlayer || c == '+')? 1: 0;
// 		beadCtr += (c == myPlayer)? 1: 0;
// 	}
// 	for(int i = 1; i <= 3 && last_x+i <= 5 && board[last_x+i][last_y] != myOpponent; i++){
// 		char c = board[last_x+i][last_y];
// 		ctr += (c == myPlayer || c == '+')? 1: 0;
// 		beadCtr += (c == myPlayer)? 1: 0;
// 	}

// 	cout<<"beadCtr: "<<beadCtr<<endl;	

// 	if(ctr >= 4){
// 		for(int i = 1; i <= 3 && last_x-i >= 0 && board[last_x-i][last_y] != myOpponent; i++){
// 			weightBoard[last_x-i][last_y] += (board[last_x-i][last_y] == '+')? beadCtr: 0;
// 		}
// 		for(int i = 1; i <= 3 && last_x+i <= 5 && board[last_x+i][last_y] != myOpponent; i++){
// 			weightBoard[last_x+i][last_y] += (board[last_x+i][last_y] == '+')? beadCtr: 0;
// 		}
// 	}

// 	ctr = 0;
// 	beadCtr = 0;
// }

// Desc: Helper of above func. Update one line on weight board, according to last x, y
// void ConnectFour::updateLine(char* line, int dx, int dy, char player){

// }

// Desc: Helper of checkWin(). Check if exist connection of 4 in the given line
char ConnectFour::checkLine(char* line, int len){
	for(int i = 0; i <= len-4; i++){
		if(line[i]!='+' && line[i+1]!='+' && line[i+2]!='+' && line[i+3]!='+' && 
			line[i] == line[i+1] && line[i+1] == line[i+2] && line[i+2] == line[i+3])
			return line[i];
	}
	return 0;
}

// Desc:  Return myPlayer/myOpponent if myPlayer/myOpponent wins, otherwise 0
char ConnectFour::checkWin(){//int x, int y
	if(checkLine(board[last_x], 7)){
		//cout<<"line win"<<endl;
		return board[last_x][last_y];
	}

	char vertical[6];
	for(int i = 0; i < 6; i++){
		vertical[i] = board[i][last_y];	
	}
	if(checkLine(vertical, 6)){
		//cout<<"vertical win"<<endl;
		return board[last_x][last_y];
	}

	char diag[7], antidiag[7];
	for(int i = 0; i < 7; i++){
		diag[i] = '+';	
		antidiag[i] = '+';
	}
	diag[3] = board[last_x][last_y]; //[] [] [] [x,y] [] [] []
	antidiag[3] = board[last_x][last_y];
	for(int i = 1; i <= 3 && last_x-i >= 0 && last_y-i >= 0; i++){
		diag[3-i] = board[last_x-i][last_y-i];
	}
	for(int i = 1; i <= 3 && last_x+i <= 5 && last_y+i <= 6; i++){
		diag[3+i] = board[last_x+i][last_y+i];
	}

	//Debug:
	// cout<<"diag: ";
	// for(int i = 0; i < 7; i++){
	// 	cout<<diag[i]<<" ";
	// }
	// cout<<endl;

	if(checkLine(diag, 7)){
		//cout<<"diag win"<<endl;
		return board[last_x][last_y];
	}

	for(int i = 1; i <= 3 && last_x+i <= 5 && last_y-i >= 0; i++){
		antidiag[3-i] = board[last_x+i][last_y-i];
	}
	for(int i = 1; i <= 3 && last_x-i >= 0 && last_y+i <= 6; i++){
		antidiag[3+i] = board[last_x-i][last_y+i];
	}

	//Debug:
	// cout<<"antidiag: ";
	// for(int i = 0; i < 7; i++){
	// 	cout<<antidiag[i]<<" ";
	// }
	// cout<<endl;

	if(checkLine(antidiag, 7)){
		//cout<<"antidiag win"<<endl;
		return board[last_x][last_y];
	}

	// bool isDraw = true;
	// for(int i = 0; i < 7; i++){
	// 	if(isAvailable(i)){
	// 		isDraw = false;
	// 	}
	// }
	if(!nAvailable){
		return 'D';//Draw
	}
	return 0;//No win and not draw

}

// Desc:  Check if position x is available to drop bead
bool ConnectFour::isAvailable(int y){
	return heights[y] < 6;
}

// Desc:  Display game board
void ConnectFour::display(){
	cout<<"-------------"<<endl;
	cout<<"1 2 3 4 5 6 7 "<<endl;
	for(int i = 5; i >= 0; i--){
		for(int j = 0; j <= 6; j++){
			cout << board[i][j] << " ";
		}
		cout << endl;
	}
	cout<<"-------------"<<endl;
}

// Desc:  Display weight board
// void ConnectFour::displayWeights(){
// 	cout<<"----------------------------------"<<endl;
// 	//cout<<"1 2 3 4 5 6 7 "<<endl;
// 	for(int i = 5; i >= 0; i--){
// 		for(int j = 0; j <= 6; j++){
// 			printf("%4.1f ", weightBoard[i][j]);
// 		}
// 		cout << endl;
// 	}
// 	cout<<"----------------------------------"<<endl;
// }