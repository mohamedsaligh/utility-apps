package com.saligh.rest.services;

import com.saligh.rest.to.Message;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.Date;
import java.util.List;

/**
 * Created by saligh on 4/2/16.
 */
@Controller
@Path("/message")
public class MessageResource {

    @Autowired
    private MessageService messageService;

    /*public void setMessageService(MessageService messageService) {
        this.messageService = messageService;
    }*/

    @GET
    @Path("ping")
    public String getServerTime() {
        System.out.println("RESTful Service 'Message Service' is running ==> ping");
        return "received ping on " + new Date().toString();
    }

    @GET
    @Produces({MediaType.APPLICATION_JSON})
    public List<Message> getAllMessages() throws Exception {
        return messageService.getAllMessages();
    }

    @POST
    @Consumes({MediaType.APPLICATION_JSON})
    @Produces({MediaType.TEXT_PLAIN})
    @Path("/post")
    public String postMessage(Message message) throws Exception {
        return messageService.postMessage(message);
    }
}
