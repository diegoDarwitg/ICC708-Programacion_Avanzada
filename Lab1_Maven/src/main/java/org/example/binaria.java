package org.example;

import java.util.Arrays;

public class binaria {
    public static void main(String[] args) {
        int[] numeros = {4, 2, 7, 1, 9, 3};
        int objetivo = 7;
        Arrays.sort(numeros);
        int inicio = 0;
        int fin = numeros.length - 1;
        boolean encontrado = false;

        while (inicio <= fin) {
            int medio = (inicio + fin) / 2;

            if (numeros[medio] == objetivo) {
                encontrado = true;
                break;
            } else if (numeros[medio] < objetivo) {
                inicio = medio + 1;
            } else {
                fin = medio - 1;
            }
        }
        System.out.println("Encontrado: " + encontrado);
    }
}
