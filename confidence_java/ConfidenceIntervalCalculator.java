import java.text.DecimalFormat;

public class ConfidenceIntervalCalculator {
    // current default T_TEST_VALUE is set to 
    // df == 4 & 95% confidence interval
    private final static double T_TEST = 2.776;
    private static final boolean DEBUG = false;
    public static String execute(double [] data){
	return execute(data, T_TEST, 2, Double.MAX_VALUE);
    }
    public static String execute(double [] data,
				 double t_value,
				 int significant,
				 double missingValue){
        String rtn = "N/N";
        double sum = 0.0;
        int size = data.length;
        for(int i = 0; i < data.length ; i += 1){
            if(data[i] == missingValue){
                size -= 1;
            }
            else {
                sum += data[i];
            }       
        }
        if(size == 0 || size == 1) return rtn;
        // s stands for "sample"
        double sMean = sum / (double) size;
        double sStandardDerivation = 0.0;
        // algorithm to calcule standard derivation
        for(int i = 0; i < data.length; i += 1){
            if(data[i] == missingValue){}
            else {
                sStandardDerivation += ((sMean - data[i]) * (sMean - data[i]));
            }
        }
        sStandardDerivation /= (double) (size - 1);
        sStandardDerivation = Math.sqrt(sStandardDerivation);
	if(DEBUG){
	    System.out.println("sMean == "
			       + sMean
			       + "\tsStandardDerivation == "
			       + sStandardDerivation);
	}
        // end of calculating standard derivation
        // t_values VALUES SHOULD CHANGE ACCORDING TO size
        // but according to Akshay, Bernard said NVM
        double interval = t_value * (sStandardDerivation / Math.sqrt(size));
	String myFormat = "#.";

	for(int i = 0; i < significant; i += 1){
	    myFormat += "#";
	}
        DecimalFormat df = new DecimalFormat(myFormat);
        rtn = df.format(sMean) + "+-" + df.format(interval);
	if(DEBUG) {
	    System.out.println("[" +(sMean + interval) + "-" + (sMean - interval) + "]");
	}
        //      System.out.println(df.format(sMean) + "+-" + df.format(interval));
        return rtn;
    }

    public static void main(String [] args){
	// this example is used to varify my program correctness
	// source of this example is
	// http://www.statisticshowto.com/articles/how-to-construct-a-confidence-interval-from-data-using-the-t-distribution/
	//double[] data = {68, 69, 74, 76, 79, 87, 88, 90, 93};
	double [] data = {45, 55, 67, 
			  Double.MAX_VALUE, 
			  45, 
			  Double.MAX_VALUE, 
			  68, 79, 98, 87, 84, 82};
	System.out.println(execute(data));
	System.out.println("hello world");
    }
}