import org.json.JSONObject;

public class question {

	int number;
	static MultiThreadServer mThreadServer;
	
		
	public void setSocket(MultiThreadServer mThreadServer){
		this.mThreadServer=mThreadServer;
	}
	
	public JSONObject createJSON2Send(String label, Object data){
		JSONObject json = new JSONObject();
		json.append(label,data);
		return json;
	}
	
	public JSONObject add2JSON(JSONObject json, String label, Object data){
		json.append(label,data);
		return json;
	}

	
	public void createAndSend(Object label, Object data){
		JSONObject json = createJSON2Send(label.toString(), data);
		//System.out.println("JSON="+json);
		int length =json.toString().length();
		//System.out.println("length:"+length);
		int lengthofLength = String.valueOf(length).length();
		//System.out.println("lengthofLength: "+lengthofLength);
		int finalength=length+lengthofLength;
		String fl=""+finalength;
		//System.out.println("l="+fl);
		//mThreadServer.send(fl+json); 
		mThreadServer.send(json); 
	}
	
	public void send(String s){
		mThreadServer.send(s); 
		//System.out.println("Sending: "+s);
	}
	
	public void send(JSONObject s){
		mThreadServer.send(s); 
		//System.out.println("Sending: "+s);
	}
}
