package com.codility.numbers;

import java.math.BigInteger;

/**
 * Created by saligh on 3/12/15.
 */
public class EquilibriumIndex {

    private static BigInteger sub = BigInteger.ZERO;
    private static BigInteger sum = BigInteger.ZERO;
    private static BigInteger left = BigInteger.ZERO;
    private static BigInteger right = BigInteger.ZERO;

    public static void main(String[] args) throws Exception {
        EquilibriumIndex eqi = new EquilibriumIndex();

        int[] A = {-1, 3, -4, 5, 1, -6, 2, 1};
        System.out.print(eqi.solution(A));

    }

    public int solution(int[] A) {

        sum = BigInteger.ZERO;
        if (A.length != -1 ) {
            sum = sum.add(sumOfSubArray(A));
        }

        for (int i=0; i<A.length; i++) {
            sub = sub.add(BigInteger.valueOf(A[i]));

            left = sub.subtract(BigInteger.valueOf(A[i]));
            right = sum.subtract(sub);

            if ( left.equals(right)) {
                return i;
            }
        }

        return -1;
    }

    public static BigInteger sumOfSubArray(int[] a) {
        BigInteger sum = BigInteger.ZERO;

        for (int i = 0; i < a.length; i++) {
            sum = sum.add(BigInteger.valueOf(a[i]));
        }

        return sum;
    }
}
