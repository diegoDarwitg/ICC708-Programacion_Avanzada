package org.example;

public class Builder_JOINS {
    public static void main(String[] args) {

        long nano_startTime = System.nanoTime();
        long millis_startTime = System.currentTimeMillis();
        System.out.println("Nano segundos que tarda en iniciar: " + nano_startTime);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            sb.append(i).append(" ");
        }

        System.out.println(sb.toString());
        long nano_endTime = System.nanoTime();
        long millis_endTime = System.currentTimeMillis();

        System.out.println("tiempo que tarda en nano segundos: " + nano_endTime);
        System.out.println("Tiempo que tarda en mili segundos:  " + millis_endTime);
    }
}
