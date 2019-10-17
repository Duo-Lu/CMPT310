
#include <stdlib.h>
#include <iostream>
#include <math.h>
#include <limits>
#include <vector>
#include "MCTS.h"
#include "ConnectFour.h"

// Desc:  Constructor
MCTS::MCTS(){}

// Desc:  Destructor
MCTS::~MCTS(){}

// Desc:  pMCTS make move
int MCTS::chooseMove_pMCTS(ConnectFour game, char myPlayer){
    
    ConnectFour *myGame = new ConnectFour(game);
    //char myPlayer = player;
    char myOpponent = 'X'+'O' - myPlayer;
    //int len = curr_game.getN_Availables();
    double* scores = new double[7];
    double bestScore = -numeric_limits<double>::infinity();//negative infinity
    int index = 0;
    for(int i = 0; i < 7; i++){
        ConnectFour myGame_copy = ConnectFour(*myGame);
        if(!myGame->isAvailable(i)){
            continue;
        }
        myGame_copy.makeMove(i, myPlayer);
        if(myGame_copy.checkWin() == myPlayer){//direct win
            return i;
        }
        scores[i] = 0.0;
    }
    for(int i = 0; i < 7; i++){
        ConnectFour myGame_copy = ConnectFour(*myGame);
        if(!myGame->isAvailable(i)){
            continue;
        }
        myGame_copy.makeMove(i, myOpponent);
        if(myGame_copy.checkWin() == myOpponent){//direct loose
            return i;
        }
    }
    for(int i = 0; i < 7; i++){
        
        if(!myGame->isAvailable(i)){
            continue;
        }
    
        ConnectFour myGame_copy = ConnectFour(*myGame);
        //ConnectFour myGame_copy2 = ConnectFour(*myGame);
        myGame_copy.makeMove(i, myPlayer);
        // myGame_copy2.makeMove(i, myOpponent);
        // if(myGame_copy.checkWin() == myPlayer){//direct win
        //     return i;
        // }
        // if(myGame_copy2.checkWin() == myOpponent){//direct loose
        //     return i;
        // }
        //cout<<"debug"<<endl;
        char curr_player = 'X'+'O' - myPlayer;
        for(int playout = 0; playout < 20000; playout++){
            ConnectFour curr_game = ConnectFour(myGame_copy);
            int nLeft = curr_game.getN_Left();
            while(!curr_game.checkWin()){
                int randIndex;
                do{//randomly choose a move
                    randIndex = rand()%7;
                }while(!curr_game.isAvailable(randIndex));
                
                curr_game.makeMove(randIndex, curr_player);
                nLeft --;

                char state = curr_game.checkWin();
                if(state == myPlayer){
                    scores[i] += nLeft;
                    break;
                }
                else if(state == myOpponent){
                    scores[i] -= 2*nLeft;
                    break;
                }
                curr_player = 'X'+'O' - curr_player;
                    
            }
        }//playout ends
        if(bestScore < scores[i]){
            bestScore = scores[i];
            index = i;
        }
    }
    
    //cout<<"scores: ";
    
    //cout<<scores[i]<<" ";
    
    //cout<<endl;

    delete myGame;
    delete[] scores;
    return index;
}

// Desc:  heuristicMCTS make move
int MCTS::chooseMove_hMCTS(ConnectFour game, char myPlayer){
    
    ConnectFour *myGame = new ConnectFour(game);
    int *heights = myGame->getHeights();
    char myOpponent = 'X'+'O' - myPlayer;
    double* scores = new double[7];
    for(int i = 0; i < 7; i++){
        scores[i] = 0.0;
    }
    double bestScore = -numeric_limits<double>::infinity();//negative infinity
    int index = 0;
    for(int i = 0; i < 7; i++){
        ConnectFour myGame_copy = ConnectFour(*myGame);
        if(!myGame->isAvailable(i)){
            continue;
        }
        myGame_copy.makeMove(i, myPlayer);
        if(myGame_copy.checkWin() == myPlayer){//direct win
            return i;
        }
        scores[i] = 0.0;
    }
    for(int i = 0; i < 7; i++){
        ConnectFour myGame_copy = ConnectFour(*myGame);
        if(!myGame->isAvailable(i)){
            continue;
        }
        myGame_copy.makeMove(i, myOpponent);
        if(myGame_copy.checkWin() == myOpponent){//direct loose
            return i;
        }
    }

    //cout<<"Scores: ";
    for(int i = 0; i < 7; i++){
        
        if(!myGame->isAvailable(i)){
            continue;
        }
    
        ConnectFour myGame_copy = ConnectFour(*myGame);
        ConnectFour myGame_copy2 = ConnectFour(*myGame);
        myGame_copy.makeMove(i, myPlayer);
        double myWeight = computeWeight(myGame_copy, myPlayer);
        double opponentWeight = computeWeight(myGame_copy, myOpponent);
        int playoutAdjustment = (int) (myWeight - opponentWeight);
        //cout<<"adj: "<<playoutAdjustment<<" ";
        int nLeft = myGame_copy.getN_Left();
        myGame_copy2.makeMove(i, myPlayer);
        for(int j = 0; j < 7; j++){
            if(!myGame_copy2.isAvailable(j)){
                continue;
            }
            myGame_copy2.makeMove(j, myOpponent);
            if(myGame_copy2.checkWin() == myOpponent){//loose after i move
                scores[i] -= 1000*(nLeft-1);
            }
        }
        
        //cout<<"debug"<<endl;
        char curr_player = 'X'+'O' - myPlayer;
        for(int playout = 0; playout < 30000+playoutAdjustment*10; playout++){ //10000+playoutAdjustment*10
            ConnectFour curr_game = ConnectFour(myGame_copy);
            nLeft = curr_game.getN_Left();
            while(!curr_game.checkWin()){
                int randIndex;
                do{//randomly choose a move
                    randIndex = rand()%7;
                }while(!curr_game.isAvailable(randIndex)); 
                //randIndex = chooseMove_weight(myGame_copy, curr_player);    
                
                curr_game.makeMove(randIndex, curr_player);
                nLeft --;

                char state = curr_game.checkWin();
                if(state == myPlayer){
                    scores[i] += nLeft;
                    break;
                }
                else if(state == myOpponent){
                    scores[i] -= 2*nLeft;
                    break;
                }
                curr_player = 'X'+'O' - curr_player;
                    
            }
        }//playout ends
        //cout<<i<<":"<<scores[i]<<" ";
        if(bestScore < scores[i]){
            bestScore = scores[i];
            index = i;
        }
    }
    //cout<<endl;

    delete myGame;
    delete[] scores;
    return index;
}

// Desc:  Make move according to weight
int MCTS::chooseMove_weight(ConnectFour game, char myPlayer){
      
    ConnectFour *myGame = new ConnectFour(game);
    //char myPlayer = player;
    char myOpponent = 'X'+'O' - myPlayer;
    //int len = curr_game.getN_Availables();
    double* scores = new double[7];
    double bestScore = -numeric_limits<double>::infinity();//negative infinity
    //cout<<"scores: ";
    int index = 0;
    for(int i = 0; i < 7; i++){
        scores[i] = 0.0;
    }

    double myScore = MCTS::computeWeight(*myGame, myPlayer);
    double opponentScore = MCTS::computeWeight(*myGame, myOpponent);


    for(int i = 0; i < 7; i++){
        
        if(!myGame->isAvailable(i)){
            continue;
        }
    
        ConnectFour myGame_copy = ConnectFour(*myGame);
        //ConnectFour myGame_copy2 = ConnectFour(*myGame);
        myGame_copy.makeMove(i, myPlayer);
        //myGame_copy2.makeMove(i, myOpponent);
        // if(myGame_copy.checkWin() == myPlayer){//direct win
        //     return i;
        // }
        // if(myGame_copy2.checkWin() == myOpponent){//direct loose
        //     return i;
        // }
        //cout<<"debug"<<endl;
        char curr_player = 'X'+'O' - myPlayer;
        double myNewScore = MCTS::computeWeight(myGame_copy, myPlayer);
        double opponentNewScore = MCTS::computeWeight(myGame_copy, myOpponent);
        scores[i] = myNewScore - myScore + 2*(opponentScore - opponentNewScore);

        if(bestScore < scores[i]){
            bestScore = scores[i];
            index = i;
        }
    }
    // double bestScore = -numeric_limits<double>::infinity();//negative infinity
    // //cout<<"scores: ";
    // int index = 0;
    // for(int i = 0; i < 7; i++){
    //     if(bestScore < scores[i] && myGame->isAvailable(i)){
    //         bestScore = scores[i];
    //         index = i;
    //     }
    //     cout<<scores[i]<<" ";
    // }
    // //cout<<endl;

    delete myGame;
    delete[] scores;
    return index;
}

// Desc:  combined two decision making approaches
int MCTS::chooseMove_combined(ConnectFour game, char myPlayer){
      
    ConnectFour *myGame = new ConnectFour(game);
    int index = 0; 
    int nLeft = myGame->getN_Left();
    if(nLeft > 35){
      index = chooseMove_weight(*myGame, myPlayer);
    }
    else{
      index = chooseMove_hMCTS(*myGame, myPlayer);
    }
    delete myGame;
    return index;
}

// Desc:  Heuristic. Calculating total weight
double MCTS::computeWeight(ConnectFour game, char myPlayer){
  char** board = game.getBoard();
  int* heights = game.getHeights();
  double totalWeight = 0.0;
  int beadCtr = 0;
  int emptySpaceCtr = 0;
  //For rows:
//  board : [5,0][5,1][5,2][5,3][5,4][5,5][5,6]
//				  [4,0][4,1][4,2][4,3][4,4][4,5][4,6]
//				  [3,0][3,1][3,2][3,3][3,4][3,5][3,6]
//				  [2,0][2,1][2,2][2,3][2,4][2,5][2,6]
//				  [1,0][1,1][1,2][1,3][1,4][1,5][1,6]
//				  [0,0][0,1][0,2][0,3][0,4][0,5][0,6]
  for(int i = 0; i < 6; i++){
    for(int j = 0; j < 7-3; j++){
      beadCtr = 0;
      emptySpaceCtr = 0;
      for(int offset = 0; offset < 4; offset ++){
        if(board[i][j+offset] == myPlayer){
          beadCtr ++;
        }
        else if(board[i][j+offset] == '+'){
          emptySpaceCtr ++;
        }
      }

      if((beadCtr+emptySpaceCtr) == 4 && emptySpaceCtr != 4){
        for(int offset = 0; offset < 4; offset ++){
          if(board[i][j+offset] == '+'){
            totalWeight += scorePerCell(beadCtr, i+1-heights[j+offset]);
          }
          else{
            totalWeight += scorePerCell(beadCtr, 0);
          }
        }
      }
    }
  }

  //For columns:
  for(int j = 0; j < 7; j++){
    for(int i = 0; i < 6-3; i++){
      beadCtr = 0;
      emptySpaceCtr = 0;
      for(int offset = 0; offset < 4; offset ++){
        if(board[i+offset][j] == myPlayer){
          beadCtr ++;
        }
        else if(board[i+offset][j] == '+'){
          emptySpaceCtr ++;
        }
      }

      if((beadCtr+emptySpaceCtr) == 4 && emptySpaceCtr != 4){
        for(int offset = 0; offset < 4; offset ++){
          if(board[i+offset][j] == '+'){
            totalWeight += scorePerCell(beadCtr, i+offset+1-heights[j]);
          }
          else{
            totalWeight += scorePerCell(beadCtr, 0);
          }
        }
      }
    }
  }

  //For diags:
  //for those lengths = 4
  int beadCtrs[4] = {0, 0, 0, 0};
  int emptySpaceCtrs[4] = {0, 0, 0, 0};
  for(int i3 = 3, i2 = 2, i5 = 5, i0 = 0; i3 >= 0; i3--, i2++, i5--, i0 ++){//i#, # refers to start x index
    if(board[i3][3-i3] == myPlayer){
      beadCtrs[0] ++;
    }
    else if(board[i3][3-i3] == '+'){
      emptySpaceCtrs[0] ++;
    }
    if(board[i2][i2-2] == myPlayer){
      beadCtrs[1] ++;
    }
    else if(board[i2][i2-2] == '+'){
      emptySpaceCtrs[1] ++;
    }
    if(board[i5][8-i5] == myPlayer){
      beadCtrs[2] ++;
    }
    else if(board[i5][8-i5] == '+'){
      emptySpaceCtrs[2] ++;
    }
    if(board[i0][i0+3] == myPlayer){
      beadCtrs[3] ++;
    }
    else if(board[i0][i0+3] == '+'){
      emptySpaceCtrs[3] ++;
    }
  }
  
  if(beadCtrs[0]+emptySpaceCtrs[0] == 4 && emptySpaceCtrs[0] != 4){
    for(int i3 = 3; i3 >= 0; i3 --){
      if(board[i3][3-i3] == '+'){
        totalWeight += scorePerCell(beadCtrs[0], i3+1-heights[3-i3]);
      }
      else{
          totalWeight += scorePerCell(beadCtrs[0], 0);
      }
    }
  }

  if(beadCtrs[1]+emptySpaceCtrs[1] == 4 && emptySpaceCtrs[1] != 4){
    for(int i2 = 2; i2 <= 5; i2 ++){
      if(board[i2][i2-2] == '+'){
        totalWeight += scorePerCell(beadCtrs[1], i2+1-heights[i2-2]);
      }
      else{
          totalWeight += scorePerCell(beadCtrs[1], 0);
      }
    }
  }
  
  if(beadCtrs[2]+emptySpaceCtrs[2] == 4 && emptySpaceCtrs[2] != 4){
    for(int i5 = 5; i5 >= 2; i5 --){
      if(board[i5][8-i5] == '+'){
        totalWeight += scorePerCell(beadCtrs[2], i5+1-heights[8-i5]);
      }
      else{
          totalWeight += scorePerCell(beadCtrs[2], 0);
      }
    }
  }

  if(beadCtrs[3]+emptySpaceCtrs[3] == 4 && emptySpaceCtrs[3] != 4){
    for(int i0 = 0; i0 <= 3; i0 ++){
      if(board[i0][i0+3] == '+'){
        totalWeight += scorePerCell(beadCtrs[3], i0+1-heights[i0+3]);
      }
      else{
          totalWeight += scorePerCell(beadCtrs[3], 0);
      }
    }
  }


  //for those lengths = 5
  for(int offset = 0; offset < 2; offset ++){
    //reset beadCtrs and emptySpaceCtrs
    for(int i = 0; i < 4; i++){beadCtrs[i] = 0; emptySpaceCtrs[i] = 0;}

    for(int i4 = 4-offset, i1 = 1+offset, i5 = 5-offset, i0 = 0+offset; i4 >= 1-offset ;i4 --, i1 ++, i5 --, i0 ++){
      if(board[i4][4-i4] == myPlayer){
        beadCtrs[0] ++;
      }
      else if(board[i4][4-i4] == '+'){
        emptySpaceCtrs[0] ++;
      }
      if(board[i1][i1-1] == myPlayer){
        beadCtrs[1] ++;
      }
      else if(board[i1][i1-1] == '+'){
        emptySpaceCtrs[1] ++;
      }
      if(board[i5][7-i5] == myPlayer){
        beadCtrs[2] ++;
      }
      else if(board[i5][7-i5] == '+'){
        emptySpaceCtrs[2] ++;
      }
      if(board[i0][i0+2] == myPlayer){
        beadCtrs[3] ++;
      }
      else if(board[i0][i0+2] == '+'){
        emptySpaceCtrs[3] ++;
      }
    }

    if(beadCtrs[0]+emptySpaceCtrs[0] == 4 && emptySpaceCtrs[0] != 4){
      for(int i4 = 4-offset; i4 >= 1-offset; i4 --){
        if(board[i4][4-i4] == '+'){
          totalWeight += scorePerCell(beadCtrs[0], i4+1-heights[4-i4]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[0], 0);
        }
      }
    }

    if(beadCtrs[1]+emptySpaceCtrs[1] == 4 && emptySpaceCtrs[1] != 4){
      for(int i1 = 1+offset; i1 <= 4+offset; i1 ++){
        if(board[i1][i1-1] == '+'){
          totalWeight += scorePerCell(beadCtrs[1], i1+1-heights[i1-1]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[1], 0);
        }
      }
    }
    
    if(beadCtrs[2]+emptySpaceCtrs[2] == 4 && emptySpaceCtrs[2] != 4){
      for(int i5 = 5-offset; i5 >= 2-offset; i5 --){
        if(board[i5][7-i5] == '+'){
          totalWeight += scorePerCell(beadCtrs[2], i5+1-heights[7-i5]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[2], 0);
        }
      }
    }

    if(beadCtrs[3]+emptySpaceCtrs[3] == 4 && emptySpaceCtrs[3] != 4){
      for(int i0 = 0+offset; i0 <= 3+offset; i0 ++){
        if(board[i0][i0+2] == '+'){
          totalWeight += scorePerCell(beadCtrs[3], i0+1-heights[i0+2]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[3], 0);
        }
      }
    }
  }

  //for those lengths = 6
  for(int offset = 0; offset < 3; offset ++){
    //reset beadCtrs and emptySpaceCtrs
    for(int i = 0; i < 4; i++){beadCtrs[i] = 0; emptySpaceCtrs[i] = 0;}

    for(int i5 = 5-offset, i0 = 0+offset; i5 >= 2-offset ;i5 --, i0 ++){
      if(board[i5][5-i5] == myPlayer){
        beadCtrs[0] ++;
      }
      else if(board[i5][5-i5] == '+'){
        emptySpaceCtrs[0] ++;
      }
      if(board[i0][i0] == myPlayer){
        beadCtrs[1] ++;
      }
      else if(board[i0][i0] == '+'){
        emptySpaceCtrs[1] ++;
      }
      if(board[i5][6-i5] == myPlayer){
        beadCtrs[2] ++;
      }
      else if(board[i5][6-i5] == '+'){
        emptySpaceCtrs[2] ++;
      }
      if(board[i0][i0+1] == myPlayer){
        beadCtrs[3] ++;
      }
      else if(board[i0][i0+1] == '+'){
        emptySpaceCtrs[3] ++;
      }
    }

    if(beadCtrs[0]+emptySpaceCtrs[0] == 4 && emptySpaceCtrs[0] != 4){
      for(int i5 = 5-offset; i5 >= 2-offset; i5 --){
        if(board[i5][5-i5] == '+'){
          totalWeight += scorePerCell(beadCtrs[0], i5+1-heights[5-i5]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[0], 0);
        }
      }
    }

    if(beadCtrs[1]+emptySpaceCtrs[1] == 4 && emptySpaceCtrs[1] != 4){
      for(int i0 = 0+offset; i0 <= 3+offset; i0 ++){
        if(board[i0][i0] == '+'){
          totalWeight += scorePerCell(beadCtrs[1], i0+1-heights[i0]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[1], 0);
        }
      }
    }
    
    if(beadCtrs[2]+emptySpaceCtrs[2] == 4 && emptySpaceCtrs[2] != 4){
      for(int i5 = 5-offset; i5 >= 2-offset; i5 --){
        if(board[i5][6-i5] == '+'){
          totalWeight += scorePerCell(beadCtrs[2], i5+1-heights[6-i5]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[2], 0);
        }
      }
    }

    if(beadCtrs[3]+emptySpaceCtrs[3] == 4 && emptySpaceCtrs[3] != 4){
      for(int i0 = 0+offset; i0 <= 3+offset; i0 ++){
        if(board[i0][i0+1] == '+'){
          totalWeight += scorePerCell(beadCtrs[3], i0+1-heights[i0+1]);
        }
        else{
          totalWeight += scorePerCell(beadCtrs[3], 0);
        }
      }
    }
  }    

  return totalWeight;

}

double MCTS::scorePerCell(int beadCtr, int adjustment){
  //adjustment *= 10;
  if(adjustment)
    return beadCtr == 1? 1.0/adjustment: beadCtr == 2? 5.0/adjustment: beadCtr == 3? 50.0/adjustment: 1000.0/adjustment;
  else
    return beadCtr == 1? 1.0: beadCtr == 2? 2.0: beadCtr == 3? 10.0: 1000.0;
    //beadCtr == 1? 1.0*beadCtr: beadCtr == 2? 2.0*beadCtr: beadCtr == 3? 10.0*beadCtr: 100.0*beadCtr;
}

