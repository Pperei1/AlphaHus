package student_player;

import hus.HusBoardState;
import hus.HusPlayer;
import hus.HusMove;

import java.util.ArrayList;
import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

import student_player.mytools.MyTools;

/** A Hus player submitted by a student. */
public class StudentPlayer extends HusPlayer {
    // variables used to keep track of limit depth to search in minimax
    private int depth = 7;
    // if at the previous move, the player took less than threshold ms to pick a move, we let it search by one extra depth next time
    private int threshold = 100;
    public StudentPlayer() { super("260512571"); }

    /** This is the primary method that you need to implement.
     * The ``board_state`` object contains the current state of the game,
     * which your agent can use to make decisions. See the class hus.RandomHusPlayer
     * for another example agent. */
    public HusMove chooseMove(HusBoardState board_state)
    {
        //keep track of search time
        long startTime = System.currentTimeMillis();
        int bestmove = 0;
        HusMove move = null;
        try{
            //use minimax with alpha beta pruning to pick a move
            bestmove = minimax((HusBoardState)board_state.clone(),true,0,depth,0,73,startTime);
        }
        catch (RuntimeException e){
            //if the search is not completed within 1800 ms, we stop it and restart minimax with a max depth of 5
            bestmove = minimax((HusBoardState)board_state.clone(),true,0,5,0,73,System.currentTimeMillis());
            //we decrease the search depth and increase the threshold since we went over time
            depth--;
            threshold = threshold+15;
        }
        move = board_state.getLegalMoves().get(bestmove);
        if(System.currentTimeMillis()-startTime<threshold){
            //increase depth and decrease threshold if the execution time from this turn was quick
            depth++;
            threshold = threshold-15;
        }
        return move;
    }

    public int minimax(HusBoardState board,boolean max,int depth,int maxdepth,int alpha,int beta, long startTime) throws RuntimeException{
        if(System.currentTimeMillis()-startTime>1800){
            throw new RuntimeException();
        }
        //check if we reached max depth
        if(depth < maxdepth){
            //if not search over all valid moves
            ArrayList<HusMove> moves = board.getLegalMoves();
            //check if the game has ended and return appropriate values
            if(moves.size()==0 && max){
                //0 is the minimal score
                return 0;
            }
            else if(moves.size()==0 && !max){
                //73 is superior to the maximum score, used to make sure this is picked if possible
                return 73;
            }
            HusBoardState current;
            int bestmove = 0;
            int currentvalue;
            //search over all valid moves
            for(int i=0;i<moves.size();i++){
                current = (HusBoardState)board.clone();
                current.move(moves.get(i));
                //evaluate the move using minimax
                currentvalue = minimax(current,!max,depth+1,maxdepth,alpha,beta,startTime);
                //update alpha beta parameters and determine if we can stop the computation or if we have to keep going
                if(max){
                    if(alpha<currentvalue){
                        alpha = currentvalue;
                        bestmove = i;
                    }
                    if(alpha>=beta){
                        if(depth == 0){
                            return i;
                        }
                        else{
                            return beta;
                        }
                    }
                }
                else{ 
                    if(beta>currentvalue){
                        beta = currentvalue;
                    }
                    if(alpha>=beta){
                        return alpha;
                    }
                }
            }
            if(depth == 0){
                return bestmove;
            }
            else{
                if(max){
                    return alpha;
                }
                else{
                    return beta;
                }
            }
        }
        else{
            //if we have reached max depth return the estimation of our value function
            return score(board.getPits()[player_id]);
        }
    }
    // the value function is the number of stones on our side of the field
    public int score(int[] pits){
        int score = 0;
        for(int i=0;i<pits.length;i++){
            score += pits[i];
        }
        return score;
    }
    // function used when i was generating data to train my neural network, not relevant to my player
    public String MakeData(HusBoardState state, HusMove m){
        String example = "";
        int [][] pits = state.getPits();
        int move = m.getPit();
        for(int i=0;i<pits.length;i++){
            for(int j=0;j<pits[i].length;j++){
                example = example+pits[i][j]+",";
            }
        }
        return example+move+"\n";
    }
}
