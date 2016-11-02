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
   volatile boolean con=false;
   
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
	   con=true;
	   while(!Thread.currentThread().isInterrupted()){
		   
		 //Client address + port 
		 String clientAddress = csocket.getRemoteSocketAddress().toString();
		 int ind=clientAddress.indexOf(":")+1;
		 String clientPort =clientAddress.substring(ind);
		 
		BufferedReader in=null;
		try {
				in = new BufferedReader(
					 new InputStreamReader(csocket.getInputStream()));  
				while (con){
			    	 String fromClient = in.readLine();
			    	 if(fromClient!=null)
			    		 System.out.println("\nClient on "+clientPort+": "+fromClient);
					
					 else 
						 con=false;
				}
		}
	      catch (IOException e) {
	         System.out.println(e);	
				System.out.println("Stoping current thread");
				Thread.currentThread().interrupt();
	         con=false;
	      }
		finally {
				try {
					System.out.println("closing BufferedReader");
					in.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
		}
	        
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