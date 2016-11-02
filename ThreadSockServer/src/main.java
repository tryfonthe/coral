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
	  
	  boolean con=false;

     Socket sock = ssock.accept();
     System.out.println("Client connected..");
     con=true;
	 
     while (con) {
	     //new Thread(new MultiThreadServer(sock)).start();
	     MultiThreadServer mS = new MultiThreadServer(sock);
	     t= new Thread(mS);//.start();
	     t.start();

	     q.setSocket(mS);
	     //q.createAndSend("CtrlMsg","TD");
	     while (true){
		     if ( sock.isClosed() ){
			     	System.out.println("con closed");
			     con=false;
			     break;
		     }
			     
	 		Scanner in = new Scanner(System.in);
			System.out.print("Please enter station : ");
			String station = in.nextLine();      
			System.out.println("You entered : " + station);
			System.out.print("Please enter message : ");
			String msg = in.nextLine();      
			System.out.println("You entered : " + msg);
			JSONObject jo = new JSONObject();
			jo.put("LC",station);
			jo.put("Msg", msg);
			q.send(jo);
			
			//q.createAndSend(1,input);
		     //q.send(input+"\n");
		     //q.send(input);
		     System.out.println("json sent...");
		     //Thread.sleep(10000);
	     }
	  }

	  //ssock.close();
   }
}
