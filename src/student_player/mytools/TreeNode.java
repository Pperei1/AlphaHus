package student_player.mytools;
import hus.HusBoardState;
import hus.HusPlayer;
import hus.HusMove;
import java.util.ArrayList;
import java.lang.Math;

public class TreeNode {
//ths class is the class of nodes found in the MCTS tree
    private int move;
    private TreeNode parent;
    private ArrayList<TreeNode> childs = new ArrayList<TreeNode>();
    //the number of times the node was visited
    private int visit = 0;
    //the value of the node
    private int value = 0;
    //boolean to indicate whether the node is a max or a min node
    private boolean isMax;

    public TreeNode(int move){
    	this.move = move;
    }

    public void addChild(TreeNode child){
    	childs.add(child);
    }

    public void setParent(TreeNode parent){
    	this.parent = parent;
    }

    public void setmax(boolean b){
        this.isMax = b;
    }

    public boolean getmax(){
        return this.isMax;
    }

    public int getVisit(){
    	return visit;
    }

    public int getValue(){
    	return value;
    }

    public void setValue(int value){
        this.value = value;
    }

    public int getMove(){
    	return move;
    }

    public TreeNode getParent(){
        return parent;
    }

    public void update(int va, int vi){
        if(this.isMax){
            value = value+vi-va;
        }
        else{
            value = value+va;
        }
        visit = visit+vi;
    }

    public void setMove(int move){
        this.move = move;
    }

    public ArrayList<TreeNode> getChilds(){
    	return childs;
    }

    public int getNumberChild(){
    	return childs.size();
    }

    public TreeNode getBestChild(double C){
    	TreeNode bestNode = childs.get(0);
    	double bestvalue = ucb(bestNode,C);
    	double currentvalue;
    	TreeNode currentNode;
    	for(int i=1;i<childs.size();i++){
    		currentNode = childs.get(i);
    		currentvalue = ucb(currentNode,C);
    		if(currentvalue>bestvalue){
    			bestvalue = currentvalue;
    			bestNode = currentNode;
    		}
    	}
    	return bestNode;
    }

    private double ucb(TreeNode child,double C){
    	return child.getValue()+C*Math.sqrt(Math.log((double)visit)/(double)child.getVisit());
    }
}
