#pragma once
#include <stdlib.h>
#include <iostream>
#include <math.h>
#include "ConnectFour.h"
using namespace std;

class MCTS {
    //private:
        
        

    public:

        // Desc:  Constructor
        MCTS();

        // Desc:  Destructor
        ~MCTS();

        // Desc:  pMCTS make move
        int chooseMove_pMCTS(ConnectFour game, char myPlayer);

        // Desc:  heuristicMCTS make move
        int chooseMove_hMCTS(ConnectFour game, char myPlayer);

        // Desc:  Make move according to weight
        int chooseMove_weight(ConnectFour game, char myPlayer);

        // Desc:  combined two decision making approaches
        int chooseMove_combined(ConnectFour game, char myPlayer);

        // Desc:  Heuristic. Calculating total weight
        static double computeWeight(ConnectFour game, char myPlayer);

        // Desc:  Helper of computeWeight.
        static double scorePerCell(int , int );

};