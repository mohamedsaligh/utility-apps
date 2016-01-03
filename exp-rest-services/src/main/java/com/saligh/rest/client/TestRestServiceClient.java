package com.saligh.rest.client;

import org.json.JSONObject;

import java.io.*;
import java.net.URL;
import java.net.URLConnection;

/**
 * Created by saligh on 4/2/16.
 */
public class TestRestServiceClient {

    public static void main(String[] args) {
        String string = "";
        try {
            InputStream crunchifyInputStream = new FileInputStream("/Users/saligh/Documents/Tools/extras/data/test1.json");
            InputStreamReader crunchifyReader = new InputStreamReader(crunchifyInputStream);
            BufferedReader br = new BufferedReader(crunchifyReader);
            String line;
            while ((line = br.readLine()) != null) {
                string += line + "\n";
            }

            JSONObject jsonObject = new JSONObject(string);
            System.out.println(jsonObject);

            try {
                URL url = new URL("http://localhost:8080/rest/api/testService");
                URLConnection connection = url.openConnection();
                connection.setDoOutput(true);
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setConnectTimeout(5000);
                connection.setReadTimeout(5000);
                OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());
                out.write(jsonObject.toString());
                out.close();

                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));

                while (in.readLine() != null) {
                }
                System.out.println("\nCrunchify REST Service Invoked Successfully..");
                in.close();
            } catch (Exception e) {
                System.out.println("\nError while calling Crunchify REST Service");
                System.out.println(e);
            }

            br.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
