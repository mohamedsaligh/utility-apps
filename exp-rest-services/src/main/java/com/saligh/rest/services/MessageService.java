package com.saligh.rest.services;

import com.saligh.rest.to.Message;

import java.util.List;

/**
 * Created by saligh on 8/2/16.
 */
public interface MessageService {

    List<Message> getAllMessages();

    String postMessage(Message message);

}
