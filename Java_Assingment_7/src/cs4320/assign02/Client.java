package cs4320.assign02;

import java.io.*;
import java.net.Socket;

/**
 * Created by Ben Setzer on 2/18/2015.
 *
 * This carries out the client tasks as specified in the assignment
 *
 */
public class Client {

    public static final int PORT = 12321;

    public static void main(String[] args) throws IOException {
        String resp1 = sendAndReceive("S8 10 -945 1689 -950 230 -25 1 1e-13");
        if(resp1.charAt(0) == 'S') {
            double val1 = Double.parseDouble(resp1.substring(1));
            System.out.println("Value returned from bisection: " + val1 );
            String resp2 = sendAndReceive("E" + val1 + " -945 1689 -950 230 -25 1");
            if(resp2.charAt(0) == 'E') {
                double val2 = Double.parseDouble(resp2.substring(1));
                System.out.println("Value returned from eval: " + val2 );
            } else {
                System.out.println("Error in evaluation call: " + resp2.substring(1));

            }
        } else {
            System.out.println("Error in bisection call: " + resp1.substring(1));
        }
    }


    /**
     * Sends a request to the server, prints it and then prints the response.
     *
     */
    public static String sendAndReceive(String request) throws IOException {
        System.out.println("request: " + request);
        Socket conn = new Socket("localhost", PORT);
        OutputStream os = conn.getOutputStream();
        Writer wr = new OutputStreamWriter(os, "UTF-8");
        wr.write(request);
        wr.flush();
        conn.shutdownOutput();

        InputStream is = conn.getInputStream();
        Reader rdr = new InputStreamReader(is,"UTF-8");
        StringBuilder sb = new StringBuilder();
        int c = rdr.read();
        while(c >= 0) {
            sb.append((char)c);
            c = rdr.read();
        }
        // System.out.println("response: " + sb);
        conn.shutdownInput();

        conn.close();
        return sb.toString();

    }


}
