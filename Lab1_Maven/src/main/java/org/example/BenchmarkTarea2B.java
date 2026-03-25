package org.example;

import org.openjdk.jmh.annotations.*;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Thread)
@Fork(1)
@Warmup(iterations = 5)
@Measurement(iterations = 20)
public class BenchmarkTarea2B {

    @Param({"10", "100", "1000", "5000", "10000", "20000"})
    public int n;

    @Benchmark
    public String testStringConcatenation() {
        String resultado = "";
        for (int i = 0; i < n; i++) {
            resultado = resultado + i + " ";
        }
        return resultado;
    }

    @Benchmark
    public String testStringBuilder() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            sb.append(i).append(" ");
        }
        return sb.toString();
    }
}