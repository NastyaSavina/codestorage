import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Mystart {
    public static void main(String[] args) throws IOException {
        List<Integer> a = new ArrayList<>();
        Process p = Runtime
                .getRuntime()
                .exec("python /Users/me/programs/scala/workplace/runPy/src/main/pyth.py Maksim");

        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
        System.out.println(in.readLine());
    }
}
