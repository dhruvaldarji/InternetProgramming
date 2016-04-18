package cs4320.assign02;

import static org.junit.Assert.*;
import org.junit.Test;

import java.io.*;
import java.net.Socket;


/**
 * Created by Ben Setzer on 2/18/2015.
 *
 * This is a client that will test the actions of the server.
 *
 * JUnit 4 must be available in order for this test to execute properly.
 *
 * Note that this test will also see how the server responds to incorrect input.
 */
public class TestJ {

    public static final int PORT = 12321;


    private static final double TOLERANCE = 1e-10;

    @Test
    public void evaluate1() throws IOException {
        String result;
        result = sendAndReceive("E1 -945 1689 -950 230 -25 1");
        assertEquals('E', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(0.0, value, TOLERANCE);
    }


    @Test
    public void evaluate2() throws IOException {
        String result;
        result = sendAndReceive("E3 -945 1689 -950 230 -25 1");
        assertEquals('E', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(0.0, value, TOLERANCE);
    }

    @Test
    public void evaluate3() throws IOException {
        String result;
        result = sendAndReceive("E5 -945 1689 -950 230 -25 1");
        assertEquals('E', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(0.0, value, TOLERANCE);
    }

    @Test
    public void evaluate4() throws IOException {
        String result;
        result = sendAndReceive("E7 -945 1689 -950 230 -25 1");
        assertEquals('E', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(0.0, value, TOLERANCE);
    }

    @Test
    public void evaluate5() throws IOException {
        String result;
        result = sendAndReceive("E9 -945 1689 -950 230 -25 1");
        assertEquals('E', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(0.0, value, TOLERANCE);
    }


    @Test
    public void bisect1() throws IOException {
        String result;
        result = sendAndReceive("S0 2 -945 1689 -950 230 -25 1 1e-10");
        assertEquals('S', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(1.0, value, TOLERANCE);
    }


    @Test
    public void bisect2() throws IOException {
        String result;
        result = sendAndReceive("S4 2 -945 1689 -950 230 -25 1 1e-10");
        assertEquals('S', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(3.0, value, TOLERANCE);
    }

    @Test
    public void bisect3() throws IOException {
        String result;
        result = sendAndReceive("S4 6 -945 1689 -950 230 -25 1 1e-10");
        assertEquals('S', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(5.0, value, TOLERANCE);
    }

    @Test
    public void bisect4() throws IOException {
        String result;
        result = sendAndReceive("S8 6 -945 1689 -950 230 -25 1 1e-10");
        assertEquals('S', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(7.0, value, TOLERANCE);
    }

    @Test
    public void bisect5() throws IOException {
        String result;
        result = sendAndReceive("S8 10 -945 1689 -950 230 -25 1 1e-10");
        assertEquals('S', result.charAt(0));
        double value = Double.parseDouble(result.substring(1));
        assertEquals(9.0, value, TOLERANCE);
    }


    @Test
    public void formatErrorExtraSpace1() throws IOException {
        String result;
        result = sendAndReceive("S8  10 -945 1689 -950 230 -25 1 1e-10");
        assertEquals('X', result.charAt(0));
    }

    @Test
    public void formatErrorExtraSpace2() throws IOException {
        String result;
        result = sendAndReceive("E8 -945 1689 -950 230  -25 1");
        assertEquals('X', result.charAt(0));
    }

    @Test
    public void formatErrorBadNumber1() throws IOException {
        String result;
        result = sendAndReceive("S8 10 -945 1689 -950a 230 -25 1 1e-10");
        assertEquals('X', result.charAt(0));
    }

    @Test
    public void formatErrorBadNumber2() throws IOException {
        String result;
        result = sendAndReceive("S8 -945 x1689 -950 230 -25 1");
        assertEquals('X', result.charAt(0));
    }

    @Test
    public void formatErrorBadOperation() throws IOException {
        String result;
        result = sendAndReceive("T8 -945 x1689 -950 230 -25 1");
        assertEquals('X', result.charAt(0));
    }


    @Test
    public void formatErrorEmptyRequest() throws IOException {
        String result;
        result = sendAndReceive("");
        assertEquals('X', result.charAt(0));
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
        //System.out.println("response: " + sb);
        conn.shutdownInput();

        conn.close();
        return sb.toString();

    }


}
