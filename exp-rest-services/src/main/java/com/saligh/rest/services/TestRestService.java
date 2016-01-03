package com.saligh.rest.services;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * Created by saligh on 4/2/16.
 */
@Path("/")
public class TestRestService {

    @POST
    @Path("/testService")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response readRestService(InputStream inputStream) {
        StringBuilder requestData = new StringBuilder();
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(inputStream));
            String line = null;
            while ((line = in.readLine()) != null) {
                requestData.append(line);
            }
        } catch (Exception e) {
            System.out.println("Error in Processing requestData: -");
        }

        System.out.println("Data as received: " + requestData.toString());

        return Response.status(200).entity(requestData.toString()).build();
    }

    @GET
    @Path("/verifyService")
    @Consumes(MediaType.TEXT_PLAIN)
    public Response verifyRestService(InputStream inputStream) {
        String responseData = "Test REST Services have been started successfully!";
        return Response.status(200).entity(responseData).build();
    }

}
