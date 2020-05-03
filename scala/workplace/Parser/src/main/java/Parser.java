import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;

public class Parser {
    public static void main(String[] args) throws IOException {
        Document doc = Jsoup.connect("https://www.w3schools.com/css/css_table.asp").get();

        Element table = doc.select("table").get(0);
        Elements rows = table.select("tr").next();

        for (Element row: rows) {
            Elements cols = row.select("td");

            System.out.println("key: " + cols.get(0).text());
            System.out.println("value: " + cols.get(1).text());
        }
    }
}
