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
public class StudentPlayer4 extends HusPlayer {
    //this player is the same as the main player, however it search to depth 7 all the time
    public StudentPlayer4() { 
        super("4"); 
    }
    public HusMove chooseMove(HusBoardState board_state)
    {
        int bestmove = 0;
        HusMove move = null;
        int depth = 1;
        bestmove = minimax((HusBoardState)board_state.clone(),true,0,depth,0,73);
        move = board_state.getLegalMoves().get(bestmove);
        return move;

        // But since this is a placeholder algorithm, we won't act on that information.
    }

    public int minimax(HusBoardState board,boolean max,int depth,int maxdepth,int alpha,int beta){
        if(depth < maxdepth){
            ArrayList<HusMove> moves = board.getLegalMoves();
            if(moves.size()==0 && max){
                return 0;
            }
            else if(moves.size()==0 && !max){
                return 73;
            }
            HusBoardState current;
            int bestmove = 0;
            int currentvalue;
            for(int i=0;(i<moves.size());i++){
                current = (HusBoardState)board.clone();
                current.move(moves.get(i));
                currentvalue = minimax(current,!max,depth+1,maxdepth,alpha,beta);
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
            return score(board.getPits()[player_id]);
        }
    }

    public int score(int[] pits){
        int score = 0;
        for(int i=0;i<pits.length;i++){
            score += pits[i];
        }
        return score;
    }

    public String MakeData(HusBoardState state, HusMove m){
        String example = "";
        int [][] pits = state.getPits();
        int move = m.getPit();
        for(int j=0;j<pits[player_id].length;j++){
            example = example+pits[player_id][j]+",";
        }
        for(int j=0;j<pits[(player_id+1)%2].length;j++){
            example = example+pits[(player_id+1)%2][j]+",";
        }
        return example+move+"\n";
    }
}
