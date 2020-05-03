package epam.mrmrmr.Nastya;

import java.util.Scanner;

public class Byla {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int max = Integer.MIN_VALUE;
        int number = 0;
        int[] array = new int[n];
        for (int i = 0; i < n; i++) {
            array[i] = i + 1;
            System.out.print("\t" + array[i]);
            if (max < array[i]) {
                max = array[i];
                number = i;
            }
        }
        System.out.println();
        System.out.println("max: " + max + " " + "number: " + number);
        int tmp = 0;
        if (n % 2 == 0) {
            for (int i = 0; i < (n / 2); i++) {
                tmp = array[i];
                array[i] = array[number-i];
                array[number-i] = tmp;
            }
        }
        if (n % 2 != 0) {
            for (int i = 0; i < n / 2; i++) {
                tmp = array[i];
                array[i] = array[number - i];
                array[number - i] = tmp;
            }
        }
        for (int i = 0; i < n; i++) {
            System.out.print("\t" + array[i]);
        }
        System.out.println();
    }
}
