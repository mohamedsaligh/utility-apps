package com.scb.cic;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.handler.HandlerCollection;
import org.eclipse.jetty.server.handler.ResourceHandler;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.webapp.WebAppContext;
import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.server.ServerProperties;
import org.glassfish.jersey.servlet.ServletContainer;
import sun.applet.Main;

import java.net.URI;
import java.net.URL;

/**
 * Hello world!
 *
 */
public class App {

    public static void main( String[] args ) throws Exception {
        ResourceConfig config = new ResourceConfig();
        config.packages("com.scb.cic");
        ServletHolder servlet = new ServletHolder(new ServletContainer(config));

        Server server = new Server(2222);
        ServletContextHandler context = new ServletContextHandler(server, "/api/*");
        context.addServlet(servlet, "/*");
        server.setHandler(context);

        // Web
        ResourceHandler webHandler = new ResourceHandler();
        webHandler.setResourceBase("./");
        webHandler.setWelcomeFiles(new String[]{"index.html"});

        // Server
        HandlerCollection handlers = new HandlerCollection();
        handlers.addHandler(context);
        handlers.addHandler(webHandler);

        server.setHandler(handlers);
        server.start();

        try {
            server.start();
            server.join();
        } finally {
            server.destroy();
        }
    }
}
