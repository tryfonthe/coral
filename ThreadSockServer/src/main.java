import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

import org.json.JSONObject;

public class main {
	
	static int port =8999; //port of the server
	static Thread t;
	
   public static void main(String args[]) throws Exception {
	  
	  ServerSocket ssock = new ServerSocket(port);
	  System.out.println("Listening on port:"+port);
	  
	  question q = new question ();
	  
	  JSONObject json = new JSONObject();
	  
	  while (true) {
	     Socket sock = ssock.accept();
	     System.out.println("Client connected..");
	     //new Thread(new MultiThreadServer(sock)).start();
	     MultiThreadServer mS = new MultiThreadServer(sock);
	     t= new Thread(mS);//.start();
	     t.start();
	     
	     q.setSocket(mS);
	     //q.createAndSend("CtrlMsg","TD");
	     while (true){
	    	 
	 		Scanner in = new Scanner(System.in);
			System.out.print("Please enter something : ");
			String input = in.nextLine();      
			System.out.println("You entered : " + input);
			
		     //q.send(input+"\n");
		     q.send(input);
		     System.out.println("sent: "+input);
		     //Thread.sleep(10000);
	     }
	  }

	  //ssock.close();
   }
}
