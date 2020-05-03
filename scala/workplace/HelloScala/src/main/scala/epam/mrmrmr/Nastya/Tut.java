package epam.mrmrmr.Nastya;

import java.util.Random;
import java.util.Scanner;

class kek {
    int a;
    kek b;
}

public class Tut {
    public static void main(String[] args) {
        int x1 = 0;
        int y1 = 0;
        int x2 = 0;
        int y2 = 2;
        int x3 = 5;
        int y3 = 2;

        kek obj1 = new kek();
        kek obj2 = new kek();

        obj2.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.b.a = 3;

        int resX = 0;
        int resY = 0;

        if (x1 == x2) {
            resX = x3;
        } else if (x1 == x3) {
                resX = x2; }
                else {
                resX = x1;
            }

    }

    public static void main2(String[] args) {
        int a = 3;
        int b = -2;
        int c = 2;

        boolean aBGreater = (a > 0) && (b > 0) && (c < 0);
        boolean aCGreater = (a > 0) && (b < 0) && (c > 0);
        boolean bCGreater = (a < 0) && (b > 0) && (c > 0);

        boolean onlyTwoGreater = aBGreater ^ bCGreater ^ aCGreater;

        System.out.println(onlyTwoGreater);
    }

    public static void main1(String[] args) {
        int a = 4;
        boolean isChetnoe = a % 2 == 0;
        System.out.println(isChetnoe);

        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int k = 7;
        int m = 5;
        int [] arrayOne = new int[k+m];
        int [] arrayTwo = new int[m];
        Random random = new Random(2);
        for (int i = 0; i < k; i++) {
                arrayOne[i]=random.nextInt(4);
                System.out.print("\t"+ arrayOne[i]);
            }
            System.out.println();
        for (int i = 0; i < m; i++) {
            arrayTwo[i]=random.nextInt(4);
            System.out.print("\t"+ arrayTwo[i]);
        }
        System.out.println();
        int val = k - 1 + m;


        for (int i = n+1; i < k; i++) {
            arrayOne[i+m] = arrayOne[i];
            val = i+m;
        }

        for (int i = n+1; i < k + m - n ; i++) {
            arrayOne[i] = arrayTwo[i-n-1];
            //arrayOne[2]=arrayTwo[0]
            //arrayOne[3]=arrayTwo[1]
            //arrayOne[4]=arrayTwo[2]
            //arrayOne[5]=arrayTwo[3] <-
        }
        for (int i = 0; i < k+m; i++) {
            System.out.print("\t"+ arrayOne[i]);
        }
        System.out.println();
        //arrayOne[2] -> arrayOne[7]
        //arrayOne[3] -> arrayOne[8]

        }


    }
