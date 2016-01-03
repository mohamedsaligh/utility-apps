package com.codility.numbers.olinetest;

import java.util.Stack;

/**
 * Created by saligh on 6/12/15.
 */
public class StackImpl {

    public static void main(String args[]) {
        // creating stack
        Stack st = new Stack();

        // populating stack
        st.push("Java");
        st.push("Source");
        st.push("code");

        // removing top object
        System.out.println("Removed object is: "+st.pop());

        // elements after remove
        System.out.println("Elements after remove: "+st);
    }

}
