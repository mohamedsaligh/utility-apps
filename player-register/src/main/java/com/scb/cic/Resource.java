package com.scb.cic;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.io.*;

/**
 * Created by saligh on 4/4/17.
 */
@Path("/home")
public class Resource {

    private String DATAFILE = "./data.txt";

    @GET
    @Path("/hello/{name}")
    @Produces(MediaType.TEXT_PLAIN)
    public String helloWorld(@PathParam("name") String name) {
        File file = new File(".");
        String path = file.getAbsolutePath();
        return "**I am bold!**! " + name + "\nFull Path: " + path;
    }

    @GET
    @Path("/players/getAll")
    @Produces(MediaType.TEXT_PLAIN)
    public String getAllPlayers(@QueryParam("_") String jsonCallback) {
        String data = getAllData();
        return "receive" + "(" + data + ")";
    }

    @POST
    @Path("/player/register")
    @Produces(MediaType.TEXT_HTML)
    public void postMethod(@FormParam("name") String name,
                             @FormParam("role") String role) {
        System.out.println("REGISTRATION: name = " + name  + ", role = " + role);
        name = name.replace(",", " ");
        addPlayer(name, role);
    }


    private String getAllData() {
        String line = "";
        String cvsSplitBy = ",";
        String data = "";
        try {
            int counter = 1;
            BufferedReader br = new BufferedReader(new FileReader(DATAFILE));
            while ((line = br.readLine()) != null) {
                // use comma as separator
                String[] read = line.split(cvsSplitBy);
                if ("".equalsIgnoreCase(data)) {
                    data = data + "{" +
                            "\"id\":" + "\"" + counter++ +"\"," +
                            "\"name\":" + "\"" + read[0] +"\"," +
                            "\"role\":" + "\"" + read[1] +"\"," +
                            "\"team\":" + "\"" + " " +"\"}";
                } else {
                    data = data + ",{" +
                            "\"id\":" + "\"" + counter++ +"\"," +
                            "\"name\":" + "\"" + read[0] +"\"," +
                            "\"role\":" + "\"" + read[1] +"\"," +
                            "\"team\":" + "\"" + " " +"\"}";
                }
            }
            System.out.println("Response: " + data );

        } catch (IOException e) {
            e.printStackTrace();
        }

        return "[" + data + "]";
    }

    private void addPlayer(String name, String role) {
        try {
            Writer writer = new BufferedWriter(new OutputStreamWriter(
                    new FileOutputStream(DATAFILE, true), "UTF-8"));
            role = role.replace(",", " ");
            writer.append(name + "," + role + "\n");
            writer.flush();
            writer.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

}
