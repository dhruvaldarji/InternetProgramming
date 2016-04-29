package cs4320.assign02;

import java.io.*;
import java.net.Socket;

/**
 * Created by Ben Setzer on 2/18/2015.
 */
public class TryoutServer {

    public static final int PORT = 12321;

    public static void main(String[] args) throws IOException {
        sendAndReceive("E1 -945 1689 -950 230 -25 1");
        sendAndReceive("E3 -945 1689 -950 230 -25 1");
        sendAndReceive("E5 -945 1689 -950 230 -25 1");
        sendAndReceive("E7 -945 1689 -950 230 -25 1");
        sendAndReceive("E9 -945 1689 -950 230 -25 1");
        sendAndReceive("S8 10 -945 1689 -950 230 -25 1 1e-10");
        sendAndReceive("S8 6 -945 1689 -950 230 -25 1 1e-10");
        sendAndReceive("S4 6 -945 1689 -950 230 -25 1 1e-10");
        sendAndReceive("S4 2 -945 1689 -950 230 -25 1 1e-10");
        sendAndReceive("S0 2 -945 1689 -950 230 -25 1 1e-10");

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
        System.out.println("response: " + sb);
        conn.shutdownInput();

        conn.close();
        return sb.toString();

    }


}
