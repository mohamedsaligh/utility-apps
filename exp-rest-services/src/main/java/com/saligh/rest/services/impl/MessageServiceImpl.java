package com.saligh.rest.services.impl;

import com.saligh.rest.services.MessageService;
import com.saligh.rest.to.Message;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Created by saligh on 8/2/16.
 */
@Service
@Configurable
public class MessageServiceImpl implements MessageService {

    @Override
    public List<Message> getAllMessages() {
        List<Message> messages = new ArrayList<>();

        Message msg = new Message();
        msg.setFirstName("Mohamed");
        msg.setLastName("Saligh");
        msg.setDate(new Date());
        msg.setText("Hello World! Message set by \"Saligh");

        messages.add(msg);

        System.out.println("getAllMessages(): found " + messages.size() + " messages on DB");
        return messages;
    }

    @Override
    public String postMessage(Message message) {
        System.out.println("First Name = " + message.getFirstName());
        System.out.println("Last Name = " + message.getLastName());

        return "OK";
    }

}
