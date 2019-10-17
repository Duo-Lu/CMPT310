
#include <iostream>
#include <string>
#include "ConnectFour.h"
#include "MCTS.h"
using namespace std;


int main () {
    ConnectFour game = ConnectFour();
    MCTS AI = MCTS();
    //ConnectFour game = ConnectFour(temp);
    char humanPlayer = 'X';
    char computerPlayer = 'O';

    char order;
    cout << "Enter 'x' or 'o' to play first or second" << endl;
    cin >> order;
    if(order == 'o' || order == 'O'){
        humanPlayer = 'O';
        computerPlayer = 'X';
    }
    else if(order != 'x' && order != 'X'){
        cout << "Invalid input, you will play X" << endl;
    }

    //X plays first
    char curr_player = 'X';

    for(int step = 0; step < 42; step++){
        game.display();
        //cout<<"Weight of X: "<< MCTS::computeWeight(game, 'X')<<endl;
        
        string input;
        int curr_move;

        if(curr_player == humanPlayer){//humanPlayer 'X'
            cout << "Player "<<curr_player<<", enter 1-7 to place a bead:\n";
            cin >> curr_move;
            while(curr_move>7 || (curr_move&&curr_move<1) || !game.isAvailable(curr_move-1)){
                cout << "*** Invalid input ***\n";
                cin.clear();
                cout << "Player "<<curr_player<<", enter 1-7 to place a bead:\n";
                cin >> curr_move;
            }
            //curr_move = AI.chooseMove_hMCTS(game, curr_player)+1;
            //curr_move = AI.chooseMove_weight(game, curr_player)+1;
            //cout<<"Computer "<<curr_player<<" plays: "<<curr_move<<endl;
            
        }
        else{
            curr_move = AI.chooseMove_hMCTS(game, curr_player)+1;
            //curr_move = AI.chooseMove_pMCTS(game, curr_player)+1;
            //curr_move = AI.chooseMove_combined(game, curr_player)+1;
            //curr_move = AI.chooseMove_weight(game, curr_player)+1;
            cout<<"Computer "<<curr_player<<" plays: "<<curr_move<<endl;

            // cout << "Player "<<curr_player<<", enter 1-7 to place a bead:\n";
            // while(!(cin >> curr_move) || curr_move>7 || (curr_move&&curr_move<1) || !game.isAvailable(curr_move-1)){
            //     cout << "*** Invalid input ***\n";
            // }

        }

        //cout<<"last X:"<<game.getLastX()<<" last Y:"<<game.getLastY()<<endl;
        game.makeMove(curr_move-1, curr_player);
        //curr_move = 0;

        char state = game.checkWin();
        //cout<<"N available: "<<game.getNAvailable()<<endl;
        //cout<<"state: "<<state<<endl;
        if(state){
            game.display();
            if(state != 'D')
                cout<<"*** Player "<<curr_player<<" wins! ***"<<endl;
            else
                cout<<"*** Draw! ***"<<endl;
            break;
        }
        curr_player = 'X'+'O' - curr_player;
    }
    
    return 0;
}

