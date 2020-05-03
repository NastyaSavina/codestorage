package Probe;

import java.util.ArrayList;

public class Main {
    private static void merge(ArrayList<Integer> a, ArrayList<Integer> b) {
        int resLen = a.size() + b.size();
        int aCounter = 0;
        int bCounter = 0;
        ArrayList<Integer> res = new ArrayList<>();
        for (int i = 0; i < resLen; i++) {
            if (a.get(aCounter) > b.get(bCounter)) {
                res.add(a.get(aCounter));
                aCounter++;
            } else {
                res.add(b.get(bCounter));
                bCounter++;
            }
        }
        a = res;
    }

    public static void main(String... args) {
        ArrayList<Integer> a = new ArrayList<Integer>();
        ArrayList<Integer> b = new ArrayList<Integer>();
        a.add(1);
        a.add(3);
        a.add(5);
        a.add(6);
        b.add(2);
        b.add(5);
        b.add(8);
        merge(a, b);
        System.out.println(a.toString());
        System.out.println(b.toString());
    }
}
