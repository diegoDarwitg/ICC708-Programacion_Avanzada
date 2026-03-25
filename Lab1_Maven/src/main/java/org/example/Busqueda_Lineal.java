package org.example;

public class Busqueda_Lineal {
    public static void main(String[] args) {
        int[] numeros = {4, 2, 7, 1, 9, 3,10,12,54,1231,213131,231231232,125234,12};
        int objetivo = 7;

        boolean encontrado = false;

        for (int num : numeros) {
            if (num == objetivo) {
                encontrado = true;
                break;
            }
        }

        System.out.println("Encontrado: " + encontrado);
    }
}
