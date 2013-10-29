/*************************************************************************
 *  Compilation:  javac Average.java
 *  Execution:    java Confidence < data.txt
 *  Dependencies: StdIn.java
 *  
 *  Reads in a sequence of real numbers, computes the mean, standard
 *  deviation and 95% approximate confidence interval.
 *
 *  Note: the two-pass formula is preferred for stability.
 *
 *  Limitations
 *  -----------
 *   - at most 100000 inputs
 * 
 *  % java Average
 *  10.0 5.0 6.0 
 *  3.0 7.0 32.0
 *  average          = 10.5
 *  sample variance  = 116.3
 *  sample stddev    = 10.784247771634329
 *  95% approximate confidence interval
 *  [ -10.637125632403283, 31.637125632403283 ]
 *
 *  % java Average
 *  0.5000000000000002 0.5000000000000001
 *  average          = 0.5000000000000002
 *  sample variance  = 1.232595164407831E-32
 *  sample stddev    = 1.1102230246251565E-16
 *  95% approximate confidence interval
 *  [ 0.5, 0.5000000000000004 ]
 *
 *
 *************************************************************************/

public class Average { 
    private static final double T_TEST = 1,96;
    public static void main(String[] args) { 
        int MAXN = 100000;
        int n = 0;
        double[] x = new double[MAXN];

        // first pass: read in data, compute sample mean
        double sumx = 0.0;
        while (!StdIn.isEmpty()) {
            x[n] = StdIn.readDouble();
            sumx  += x[n];
            n++;
        }
        double xbar = sumx / n;

        // second pass: compute sample variance
        double xxbar = 0.0;
        for (int i = 0; i < n; i++) {
            xxbar += (x[i] - xbar) * (x[i] - xbar);
        }
        double variance = xxbar / (n - 1);
        double stddev = Math.sqrt(variance);
        double lo = xbar - T_TEST * stddev;
        double hi = xbar + T_TEST * stddev;

        // print results
        System.out.println("average          = " + xbar);
        System.out.println("sample variance  = " + variance);
        System.out.println("sample stddev    = " + stddev);
        System.out.println("95% approximate confidence interval");
        System.out.println("[ " + lo + ", " + hi + " ]");
    }
}