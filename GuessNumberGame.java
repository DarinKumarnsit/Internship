/*
 * GuessNumberGame is simulates a guessing game of which a user guesses numbers between 1 to 10
 * The answer is randomly generated then a user enters a number via the console.
 * Each time that a user enters an input, these outputs will be displayed.
 *
 * Author: Darin Kumarnsit
 * ID: 623040249-6
 * Sec: 2
 * Date: January 14, 2021
 *
 */
package kumarnsit.darin.lab3;

import java.util.Scanner;
public class GuessNumberGame {
    public static void main(String[] args) {
       //set the range between (1-10)
        int minNum = 1, maxNum = 10, correctNum;
       //random the number
        correctNum = minNum + (int) (Math.random() * ((maxNum - minNum) + 1));

        //use for loop to set the times to loop operation
        for (int play_num = 1; play_num <= 3; play_num++) {
            //get guess number that input from user
            Scanner scan = new Scanner(System.in);
            System.out.print("Please enter a guess (1-10): ");
            int guess_input = scan.nextInt();

            //if user guess the correct number so print Congratulations! and quit the program.
            if (guess_input == correctNum){
                System.out.println("Congratulations!  That's correct");
                System.exit(0);
            }
            //if user guess the number lower than the correct number so print hint to try again
            else if (guess_input < correctNum) {
                System.out.println("Please type a higher number! Number of remaining tries: " + (3-play_num));
            }
            //if user guess the number higher than the correct number so print hint to try again
            else if (guess_input > correctNum) {
                System.out.println("Please type a lower number! Number of remaining tries: " + (3-play_num));
            }
            //quit the program if user guess the number more than 3 times
            if (play_num >= 3) {
                System.exit(0);
            }
        }
    }
}