package org.example;

public class concatenación_repetida {
    public static void main(String[] args){
        long nano_startTime = System.nanoTime();
        long millis_startTime = System.currentTimeMillis();

        System.out.println("Tiempo que tarda en iniciar: " + nano_startTime);
        String resultado="";
        for (int i = 0; i < 10; i++) {
            resultado = resultado + i + " ";
        }
        System.out.println(resultado);
        long nano_endTime = System.nanoTime();
        long millis_endTime = System.currentTimeMillis();

        System.out.println("tiempo que tarda en ejecutar nano segundos: " + nano_endTime);
        System.out.println("Tiempo que tarda en ejecutar mili segundos:  " + millis_endTime);
    }
}