
package student_player;

import hus.HusBoardState;
import hus.HusPlayer;
import hus.HusMove;
import student_player.StudentPlayer4;
import boardgame.Board;

import java.util.ArrayList;
import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

import student_player.mytools.MyTools;
//class created to play games between two players and record 
//the (board,move) pair played by each player in order to train my neural network
public class makeData{
	public static void main(String [] args){
		StudentPlayer2 player1 = new StudentPlayer2();
		StudentPlayer5 player2 = new StudentPlayer5();
		HusBoardState state;
		for(int i=0;i<10;i++){
			state = new HusBoardState();
			player1.setColor(0);
			player2.setColor(1);
			while(state.getWinner() == Board.NOBODY){
				if(state.getTurnPlayer() == 0){
					state.move(player1.chooseMove(state));
				}
				else{
					state.move(player2.chooseMove(state));
				}
			}
			System.out.println("game "+i);
		}
	}
}