package com.saligh.rest.services;

import com.saligh.rest.to.Person;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by saligh on 4/2/16.
 */
@Path("/person")
public class PersonResource {

    @GET
    @Produces({MediaType.APPLICATION_JSON})
    @Path("get")
    public Person getPerson() throws Exception {
        Person person = new Person();
        person.setFirstName("Mohamed");
        person.setLastName("Saligh");
        person.setDateOfBirth(new Date());
        person.setCitizenships(new String[]{"Indian", "Singaporean"});

        Map<String, Object> cards = new HashMap<>();
        cards.put("MasterCard", "1234 1234 1234 1234");
        cards.put("Visa", "0000 0000 0000 0000");
        cards.put("Dummy", true);
        person.setCreditCards(cards);

        System.out.println("getPerson(): RESTcall on...");

        return person;
    }

    @POST
    @Consumes({MediaType.APPLICATION_JSON})
    @Produces({MediaType.TEXT_PLAIN})
    @Path("/post")
    public String postPerson(Person person) throws Exception {
        System.out.println("First Name = " + person.getFirstName());
        System.out.println("Last Name = " + person.getLastName());

        return "OK";
    }

}
