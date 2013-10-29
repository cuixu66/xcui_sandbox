import java.io.File;
import java.util.Scanner;
import java.text.DecimalFormat;

public class calCI {
    // default run_count_base should be 3, change later
    private static final int RUN_COUNT_BASE = 3;
    // SIZE & T_TEST value is corelated!
    private static final int SIZE = 5;
    private static double [] missRates = new double[SIZE];
    private static double [] rejectRates = new double[SIZE];
    private static String dirName;

    private static void init(){
	for(int i = 0; i < SIZE; i += 1){
	    missRates[i] = Double.MAX_VALUE;
	    rejectRates[i] = Double.MAX_VALUE;
	}
    }        

    private static void populateRates(int clientNum,
				      int acPercNum,
				      int offset,
				      int runCount)throws Exception {
	final String HOME_DIR = System.getProperty("user.home");
	final String BASE_DIR = HOME_DIR 
	    + "/tmp/sandbox/gnuplot/dfs"
	    + "/xcui_scripts/test_results/"
	    + dirName + "/";
	File inputFile =
	    new File(BASE_DIR +
		     "client_" + clientNum + 
		     "_acPerc_" + acPercNum +
		     "_offset_" + offset +
		     "_runCount_" + runCount);
	Scanner scanner =
	    new Scanner(inputFile);
	while(scanner.hasNextLine()){
	    String line = scanner.nextLine();
	    if(line.contains("REJECTED-PERCENTAGE")){
		line = line.substring(line.lastIndexOf(",") + 1, line.length());
		double rejectR = Double.parseDouble(line);
		//System.out.println(rejectR);
		rejectRates[runCount  - RUN_COUNT_BASE] = rejectR;
	    }
	    if(line.contains("[DEADLINE-MISSED], Overall-Percentage,")){
		line = line.substring(line.lastIndexOf(",") + 1, line.length());
		double missedR = Double.parseDouble(line);		
		//System.out.println(missedR);
		missRates[runCount - RUN_COUNT_BASE] = missedR;
	    }
	}
	scanner.close();		       
    }

    public static void main(String [] args){
	int acPercNumUpper = 90;
	int acPercNumLower = 50;
	int acPercIncr = 10;
	int clientNumUpper = 48;
	int clientNumLower = 12;
	int clientNumIncr = 12;

	int offset = 0;
	

	if(args.length != 7) {
	    System.err.println("Need the following paramemeter:\n"
			       + "<String> directoryName"
			       + "<int> acPercNumUpper"
			       + "<int> acPercNumLower"
			       + "<int> acPercIncr"
			       + "<int> clientNumUpper"
			       + "<int> clientNumLower"
			       + "<int> clientNumIncr");
	    
	    System.exit(-1);
	}
	dirName = args[0];
	acPercNumUpper = Integer.parseInt(args[1]);
	acPercNumLower = Integer.parseInt(args[2]);
	acPercIncr = Integer.parseInt(args[3]);
	clientNumUpper = Integer.parseInt(args[4]);
	clientNumLower = Integer.parseInt(args[5]);
	clientNumIncr = Integer.parseInt(args[6]);
	System.err.println("running with"
			   + " acPercNumUpper=" + acPercNumUpper
			   + " acPercNumLower=" + acPercNumLower
			   + " acPercNumIncr=" + acPercIncr
			   + " clientNumUpper=" + clientNumUpper
			   + " clientNumLower=" + clientNumLower
			   + " clientNumIncr=" + clientNumIncr);
	System.out.print("##c\\p");
	for(int acPercNum = acPercNumLower;
	    acPercNum <= acPercNumUpper;
	    acPercNum += acPercIncr) {
	    System.out.print("\t" + acPercNum);
	}
	System.out.println();
	    
	for(int clientNum = clientNumLower;
	    clientNum <= clientNumUpper;
	    clientNum += clientNumIncr){
	    System.out.print(clientNum * 4);
	    for(int acPercNum = acPercNumLower;
		acPercNum <= acPercNumUpper;
		acPercNum += acPercIncr){
		init();
		for(int runCount = RUN_COUNT_BASE;
		    runCount < RUN_COUNT_BASE + SIZE; runCount += 1){
		    try {
			populateRates(clientNum, acPercNum, offset, runCount);
			//calCI(missRates);
			//calCI(rejectRates);
		    } catch (Exception e){
			e.printStackTrace();
		    }
		}
		String outString = ConfidenceIntervalCalculator.execute(missRates);
		//		System.out.println(outString);
		outString = outString.substring(0, outString.indexOf("+-"));
		outString += " ";
		outString += ConfidenceIntervalCalculator.execute(rejectRates);
		outString = outString.substring(0, outString.indexOf("+-"));
		System.out.print("\t" + outString);
	    }
	    System.out.println();
	}
    }
}