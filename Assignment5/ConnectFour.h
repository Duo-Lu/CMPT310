
#pragma once
#include <stdlib.h>
#include <iostream>
#include <math.h>
using namespace std;

class ConnectFour {
    private:
        
        char** board;  //7*6 game board
//  	  board : [5,0][5,1][5,2][5,3][5,4][5,5][5,6]
//				  [4,0][4,1][4,2][4,3][4,4][4,5][4,6]
//				  [3,0][3,1][3,2][3,3][3,4][3,5][3,6]
//				  [2,0][2,1][2,2][2,3][2,4][2,5][2,6]
//				  [1,0][1,1][1,2][1,3][1,4][1,5][1,6]
//				  [0,0][0,1][0,2][0,3][0,4][0,5][0,6]
        //double** weightBoard;
        
        int* heights;
        // char myPlayer;       
        // char myOpponent; 
        char curr_player; 
        int last_x;
        int last_y;
        int nAvailable; 
        int nLeft;
       
        // Desc: Helper of checkWin(). Check if exist connection of 4 in the given line
       	char checkLine(char*, int );

        // Desc: Update weight board, according to last x, y
        //void updateWeight(char );

        // Desc: Helper of above func. Update one line on weight board, according to last x, y and dx, dy
        //void updateLine(char*, int, int, char );

    public:
        // Desc:  Constructor
        ConnectFour();

        // Desc:  Copy constructor
        ConnectFour(const ConnectFour &rhs);

        // Desc:  Destructor
        ~ConnectFour();

        // Desc:  Set current player
        void setPlayer(char );

        // Desc:  Get coordinate x of last move
        int getLastX();

        // Desc:  Get coordinate y of last move
        int getLastY();

        // Desc:  Get number of available moves
        int getN_Availables();

        // Desc:  Get heights of columns
        int * getHeights();

        // Desc:  Get game board 
        char ** getBoard();

        // Desc:  Get number of empty entries
        int getN_Left();

        // Desc:  Make a move at column y(y in [0,6]) of player
        int makeMove(int , char );

        // Desc:  Make a move at column y(y in [0,6]) of player, does not update weights (used for AI playouts)
        //		  Return x coordinate
        //int makeMove_unweight(int y, char player);

        // Desc:  Return myPlayer/myOpponent if myPlayer/myOpponent wins, or 'D' for draw, otherwise 0	  
      	char checkWin();

      	// Desc:  Check if position y is available to drop bead
      	bool isAvailable(int );

      	// Desc:  Display game board
      	void display();

        // Desc:  Display weight board
      	//void displayWeights();

      	// Desc:  pMCTS make move
        // static int makeMove_AI(ConnectFour game, char myPlayer){
        //     ConnectFour myGame = ConnectFour(game);
        //     //char myPlayer = player;
        //     char myOpponent = 'X'+'O' - myPlayer;
        //     //int len = curr_game.getN_Availables();
        //     double* scores = new double[7];
        //     for(int i = 0; i < 7; i++){
        //         scores[i] = 0.0;
        //     }

        //     for(int i = 0; i < 7; i++){
        //         if(!myGame.isAvailable(i)){
        //             continue;
        //         }
        //         ConnectFour myGame_copy = ConnectFour(myGame);
        //         ConnectFour myGame_copy2 = ConnectFour(myGame);
        //         myGame_copy.makeMove(i, myPlayer);
        //         myGame_copy2.makeMove(i, myOpponent);
        //         if(myGame_copy.checkWin() == myPlayer){//direct win
        //             return i;
        //         }
        //         if(myGame_copy2.checkWin() == myOpponent){//direct loose
        //             return i;
        //         }

        //         char curr_player = 'X'+'O' - myPlayer;
        //         for(int playout = 0; playout < 10000; playout++){
        //             ConnectFour curr_game = ConnectFour(myGame_copy);
        //             int nLeft = curr_game.getN_Left();
        //             while(!curr_game.checkWin()){
        //                 int randIndex;
        //                 do{//randomly choose a move
        //                     randIndex = rand()%7;
        //                 }while(!curr_game.isAvailable(randIndex));
                        
        //                 curr_game.makeMove(randIndex, curr_player);
        //                 nLeft --;

        //                 char state = curr_game.checkWin();
        //                 if(state == myPlayer){
        //                     scores[i] += nLeft;
        //                     break;
        //                 }
        //                 else if(state == myOpponent){
        //                     scores[i] -= nLeft;
        //                     break;
        //                 }
        //                 curr_player = 'X'+'O' - curr_player;
                            
        //             }
        //         }//playout ends
        //     }
        //     double bestScore = -999999.0;
        //     cout<<"scores: ";
        //     int index = 0;
        //     for(int i = 0; i < 7; i++){
        //         if(bestScore < scores[i] && myGame.isAvailable(i)){
        //             bestScore = scores[i];
        //             index = i;
        //         }
        //         cout<<scores[i]<<" ";
        //     }
        //     cout<<endl;

        //     delete scores;
        //     return index;
        // }
};


