package com.saligh.rest.to;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.Date;
import java.util.Map;

/**
 * Created by saligh on 4/2/16.
 */
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class Person {

    private String firstName;
    private String lastName;
    private Date dateOfBirth;
    private String[] citizenships;
    private Map<String, Object> creditCards;
    private int age;

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Date getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(Date dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public String[] getCitizenships() {
        return citizenships;
    }

    public void setCitizenships(String[] citizenships) {
        this.citizenships = citizenships;
    }

    public Map<String, Object> getCreditCards() {
        return creditCards;
    }

    public void setCreditCards(Map<String, Object> creditCards) {
        this.creditCards = creditCards;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
