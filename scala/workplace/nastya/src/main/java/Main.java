import java.util.ArrayList;

public class Main {
    private static void wtf(ArrayList<Integer> a, ArrayList<Integer> b) {
        int i = 0;
        int j = 0;
        int count=0;
        while ((i < a.size())&&(j< b.size())) {
            while ((j<b.size())&&( b.get(j) <= a.get(i))) {
                a.add(i, b.get(j));
                j++;
                i++;
                count++;
            }
            i++;
            if (i >= a.size()) {
                while (j != b.size()) {
                    a.add(b.get(j));
                    j++;
                    count++;
                }

                j++;
            }
            count++;

        }
        System.out.println(count);
    }
}
