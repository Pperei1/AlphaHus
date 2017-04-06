package student_player;

import hus.HusBoardState;
import hus.HusPlayer;
import hus.HusMove;
import java.util.Random;

import java.util.ArrayList;

import student_player.mytools.TreeNode;

/** A Hus player submitted by a student. */
public class StudentPlayer3 extends HusPlayer {
    //ths player was used to test out the monte carlo tree search method
    public StudentPlayer3() { super("260512571"); }

    public HusMove chooseMove(HusBoardState board_state)
    {
        //keep track of execution time
        long startTime = System.currentTimeMillis();
        //get the best move according to our monte carle tree search 
        int bestmove = mcsTree((HusBoardState)board_state.clone(),startTime);
        return board_state.getLegalMoves().get(bestmove);
    }

    public int mcsTree(HusBoardState board,long startTime){
        //initiate the search tree
        double C = 1;
        int score = score(board.getPits()[player_id]);
        TreeNode head = new TreeNode(0);
        head.setmax(true);
        TreeNode leaf;
        HusBoardState current;
        HusBoardState roll;
        TreeNode child = null;
        int move;
        int count = 0;
        //keep searching until 20 ms are left
        while(System.currentTimeMillis()-startTime<20){
            current = (HusBoardState)board.clone();
            //select best leaf based on UCT method and update the board
            leaf = selection(current,head,C);
            //check if the leaf constitutes a win for either player
            if(current.gameOver()){
                if(current.getWinner()==player_id){
                    updateTree(leaf,1,1);
                }
                else{
                    updateTree(leaf,0,1);
                }
            }
            else{
                //search over all legal moves at the leaf
                int limit = current.getLegalMoves().size();
                int update = 0;
                int visit = 0;
                for(int j=0;j<limit;j++){
                    //add a leaf for each move
                    child = new TreeNode(j);
                    leaf.addChild(child);
                    child.setParent(leaf);
                    child.setmax(!child.getParent().getmax());
                    roll = (HusBoardState)current.clone();
                    roll.move(roll.getLegalMoves().get(child.getMove()));
                    //evaluate the new leaf using the roolout method
                    if(rollout(roll,score)){
                        //if the leaf is a win for the current player, update our value count by 1
                        child.setValue(1);
                        update++;
                    }
                    //increment visit by the number of new leafs
                    visit++;
                }
                //update the values in the tree
                updateTree(child.getParent(),update,visit); 
            }
        }
        //select the best move
        return head.getBestChild(C).getMove();
    }
    //method that searchs the tree for the best leaf
    private TreeNode selection(HusBoardState board,TreeNode node,double C){
        TreeNode bestchild;
        if(node.getNumberChild()==0){
            return node;
        }
        else{
            bestchild = node.getBestChild(C);
            board.move(board.getLegalMoves().get(bestchild.getMove()));
            return selection(board,bestchild,C);
        }
    }
    // this method compares the number of stones on the player side before the move was played and after.
    //if the amount of stones has increased, we evaluate associate this with a value of 1, otherwise 0 for the player
    //the evaluation method replaces the usual rollout since we do not have enough time to simulate enough games.
    private boolean rollout(HusBoardState board,int score){
        if(score(board.getPits()[player_id])<=score){
            return false;
        }
        else{
            return true;
        }
    }
    //the method backpropagates the results up the tree
    private void updateTree(TreeNode node, int value, int visit){
        while(node.getParent()!=null){
            node.update(value,visit);
            node = node.getParent();
        }
    }

    public int score(int[] pits){
        int score = 0;
        for(int i=0;i<pits.length;i++){
            score += pits[i];
        }
        return score;
    }
}
