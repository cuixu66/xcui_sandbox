import java.io.File;
import java.util.Scanner;
import java.io.FileInputStream;

public class Test {
    public static void main(String argv[]) throws Exception{
	int open_file = 40960;

	for(int i = 0; i < open_file; i += 1){
	    File f = new File("open_file");
	    //	    Scanner scanner = new Scanner(f);
	    FileInputStream fis = new FileInputStream(f);
	}
	//	while(true){}
	System.out.println("hello world");
    }
}

