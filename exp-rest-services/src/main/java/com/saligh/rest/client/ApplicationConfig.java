package com.saligh.rest.client;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;
import java.util.*;

/**
 * Created by saligh on 4/2/16.
 */
@ApplicationPath("/service")
public class ApplicationConfig extends Application {

    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> resources = new HashSet<>();
        System.out.println("REST configuration starting: getClasses()");

        resources.add(org.glassfish.jersey.jackson.JacksonFeature.class);
        //we could also use this:
        //resources.add(com.fasterxml.jackson.jaxrs.json.JacksonJaxbJsonProvider.class);

        resources.add(com.saligh.rest.utils.JacksonJsonProvider.class);
        resources.add(com.saligh.rest.services.PersonResource.class);
        resources.add(com.saligh.rest.services.MessageResource.class);

        System.out.println("REST Configuration completed successfully!");

        return resources;
    }

    @Override
    public Set<Object> getSingletons() {
        return Collections.emptySet();
    }


    public Map<String, Object> getProperties() {
        Map<String, Object> properties = new HashMap<>();
        properties.put("jersy.config.server.wadl.disableWadl", true);

        return properties;
    }

}
