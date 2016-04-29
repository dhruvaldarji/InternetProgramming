package cs4320.assign02;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.DoubleSummaryStatistics;

/**
 * Created by Ben Setzer on 2/18/2015.
 *
 * This carries out the server tasks as specified in the assignment.
 *
 */
public class Server {

    public static final int PORT = 12321;

    public static void main(String[] args) throws IOException {
        ServerSocket ss = new ServerSocket(PORT);
        while(true) {
            Socket conn = ss.accept();

            Reader rdr = new InputStreamReader(conn.getInputStream(), "UTF-8");
            StringBuilder sb = new StringBuilder();
            int c = rdr.read();
            while(c >= 0) {
                sb.append((char)c);
                c = rdr.read();
            }
            conn.shutdownInput();
            String req = sb.toString();
            System.out.println("request: " + req );

            String response = "response was not set properly";
            if(req.length() == 0) {
                response = "XInvalid request syntax: first character should be the operation code";
            } else if(req.charAt(0) == 'E') {
                String[] params = req.substring(1).split(" ");
                if(params.length < 1) {
                    response = "XInvalid request syntax: wrong number of fields in request";
                } else {
                    try {
                        double x = Double.parseDouble(params[0]);
                        double poly[] = new double[params.length-1];
                        for (int i = 1  ; i < params.length; i++) {
                            poly[i-1] = Double.parseDouble(params[i]);
                        }
                        response = "E" + evaluate(x, poly);
                    } catch (NumberFormatException nfe) {
                        response = "Xinvalid format numeric data";
                    }
                }
            } else if(req.charAt(0) == 'S') {
                String[] params = req.substring(1).split(" ");
                if(params.length < 3) {
                    System.out.println("params length " + params.length);
                    response = "XInvalid request syntax: wrong number of fields in request";
                } else {
                    try {
                        double a = Double.parseDouble(params[0]);
                        double b = Double.parseDouble(params[1]);
                        double tol = Double.parseDouble(params[params.length-1]);
                        double poly[] = new double[params.length-3];
                        for (int i = 2  ; i < params.length-1; i++) {
                            poly[i-2] = Double.parseDouble(params[i]);
                        }
                        response = "S" + bisection(a,b,poly,tol);
                    } catch (NumberFormatException nfe) {
                        response = "Xinvalid format numeric data";
                    } catch (IllegalArgumentException iae) {
                        response = "X" + iae.getMessage();
                    }

                }
            } else {
                response = "XInvalid operation code |" + req.charAt(0) + "|";
            }

            Writer wrt = new OutputStreamWriter(conn.getOutputStream(), "UTF-8");
            wrt.write(response);
            wrt.flush();
            conn.shutdownOutput();
            conn.close();
        }
    }

    private static double evaluate(double x, double[] poly) {
//        System.out.println("evaluate x " + x );
//        System.out.print("evaluate poly ");
//        for(double cc : poly) {
//            System.out.print(cc + " ");
//        }
//        System.out.println();
        double val = 0.0;
        for( int i = poly.length-1; i >= 0; i--) {
            val = val * x  + poly[i];
        }
        return val;
    }

    private static double bisection(double a, double b, double[] poly, double tolerance) {
        if(evaluate(a, poly) > 0 ){
            throw new IllegalArgumentException("Value of polynomial at a must be non-positive: " + a + " -> " + evaluate(a,poly));
        }
        if(evaluate(b, poly) < 0 ){
            throw new IllegalArgumentException("Value of polynomial at b must be non-negative: " + b + " -> " + evaluate(b,poly));
        }
        while(Math.abs(b-a) > tolerance) {
            double mid = (a+b)/2;
            double val = evaluate(mid, poly);
            if( val <= 0)
                a = mid;
            else
                b = mid;
        }
        return (a+b)/2;
    }


}
