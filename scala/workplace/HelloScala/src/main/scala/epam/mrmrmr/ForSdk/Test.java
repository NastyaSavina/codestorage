package epam.mrmrmr.ForSdk;

import java.util.Arrays;
import java.util.Random;

public class Test {
    public static void main1(String[] args) {
        int[][] arr = new int[20][20];

        Random random = new Random();
        int count;

        for (int i = 0; i < 100; i++) {
            count = 0;
            for (int j = 0; j < 4; j++) {
                if (count < i) {

                }
            }
        }



    }

    private static int[] getColByNumber(int[][] from, int height, int colNum) {
        int[] res = new int[height];

        for (int i = 0; i < height; i++) {
            res[i] = from[i][colNum];
        }

        return res;
    }


    public static void main(String[] args) {
        int w = 7;
        int h = 7;
        int[][] arr = new int[h][w];

        int x = w / 2 + 1;
        int y = 0;
        int num = 1;

        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                arr[i][j] = 0;
            }
        }

        for (int i = 0; i < w * h; i++) {
            arr[y][x] = num;

            if (arr[nextY(y, h)][nextX(x,w)] == 0) {
                x = nextX(x, w);
                y = nextY(y, h);
            } else {
                y = underY(y, h);
            }

            num++;
        }

        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                System.out.print("\t" + arr[i][j]);
            }
            System.out.println();
        }
    }

    private static int nextX(int _x, int _w) {
        if (_x + 1 > _w - 1) {
            _x = 0;
        } else {
            _x++;
        }

        return _x;
    }

    private static int nextY(int _y, int _h) {
        if (_y - 1 < 0) {
            _y = _h - 1;
        } else {
            _y--;
        }

        return _y;
    }

    private static int underY(int _y, int _h) {
        if (_y + 1 > _h - 1) {
            _y = 0;
        } else {
            _y++;
        }

        return _y;
    }
}
