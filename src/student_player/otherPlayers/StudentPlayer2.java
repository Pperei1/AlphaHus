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
public class StudentPlayer2 extends HusPlayer {
    /** You must modify this constructor to return your student number.
     * This is important, because this is what the code that runs the
     * competition uses to associate you with your agent.
     * The constructor should do nothing else. */
    private int depth = 7;
    private int threshold = 100;
    public StudentPlayer2() { super("260512571"); }

    /** This is the primary method that you need to implement.
     * The ``board_state`` object contains the current state of the game,
     * which your agent can use to make decisions. See the class hus.RandomHusPlayer
     * for another example agent. */
    public HusMove chooseMove(HusBoardState board_state)
    {
        //similar to studentPlayer, was sued to test different value functions
        long startTime = System.currentTimeMillis();
        System.out.println(depth);
        int bestmove = 0;
        HusMove move = null;
        try{
            bestmove = minimax((HusBoardState)board_state.clone(),true,0,depth,0,73,startTime);
        }
        catch (RuntimeException e){
            bestmove = minimax((HusBoardState)board_state.clone(),true,0,5,0,73,System.currentTimeMillis());
            depth --;
            threshold = threshold+15;
        }
        move = board_state.getLegalMoves().get(bestmove);
        if(System.currentTimeMillis()-startTime<threshold){
            depth++;
            threshold = threshold-15;
        }
        return move;

        // But since this is a placeholder algorithm, we won't act on that information.
    }

    public int minimax(HusBoardState board,boolean max,int depth,int maxdepth,int alpha,int beta, long startTime) throws RuntimeException{
        if(System.currentTimeMillis()-startTime>1800){
            throw new RuntimeException();
        }
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
            for(int i=0;i<moves.size();i++){
                current = (HusBoardState)board.clone();
                current.move(moves.get(i));
                currentvalue = minimax(current,!max,depth+1,maxdepth,alpha,beta,startTime);
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
    
    //only difference with studentPlayer
    public int score(int[] pits){
        int score = 0;
        for(int i=0;i<pits.length;i++){
            score += pits[i];
        }
        for(int i=0;i<16;i++){
            if(pits[31-i]==0){
                score = score+pits[i];
            }
        }
        return score;
    }

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
