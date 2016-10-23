import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.Reader;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.SocketException;


public class MultiThreadServer implements Runnable {
   Socket csocket;
   static int port = 8999;
   
   MultiThreadServer(Socket csocket) throws IOException {
      this.csocket = csocket;
      //this.port = port;
   }

   /*
   public static void main(String args[]) 
   throws Exception {
      ServerSocket ssock = new ServerSocket(port);
      System.out.println("Listening on port:"+port);
      while (true) {
         Socket sock = ssock.accept();
         System.out.println("Client connected..");
         new Thread(new MultiThreadServer(sock)).start();
         
      }
      //ssock.close();
   }
   */
   
   //waiting to receive data
   public void run(){ 
	   SocketAddress iAdr = csocket.getLocalSocketAddress() ;
	   try {
	    	  while(true){
	    	 
	    		 //Client address + port 
		    	 String clientAddress = csocket.getRemoteSocketAddress().toString();
		    	 int ind=clientAddress.indexOf(":")+1;
		    	 String clientPort =clientAddress.substring(ind);

		    	 
		    	 BufferedReader in = new BufferedReader(
		    			 new InputStreamReader(csocket.getInputStream()));
		    	 
		    	 String fromClient = in.readLine();
		    	 System.out.println();
		         System.out.println("Client on "+clientPort+": "+fromClient);
	    	  }
	      }
	      catch (IOException e) {
	         System.out.println(e);
	      }
   }
   
   
   //send data to client
   public void send(Object data) {
      try {
         PrintStream pstream = new PrintStream
         (csocket.getOutputStream());
         
         pstream.println( data);
         
         //pstream.close();
         //csocket.close();
      }
      catch (IOException e) {
         System.out.println(e);
      }
   }

}