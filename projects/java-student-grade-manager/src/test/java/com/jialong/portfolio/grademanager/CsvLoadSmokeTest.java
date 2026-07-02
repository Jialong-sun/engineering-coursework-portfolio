package com.jialong.portfolio.grademanager;

import java.util.List;

public final class CsvLoadSmokeTest {
    private CsvLoadSmokeTest() {
    }

    public static void main(String[] args) {
        List<Student> students = new StudentLoader().readStudentInfo("data/student_scores_sample.csv");
        require(students.size() == 10, "Expected 10 anonymized sample records.");

        Student first = students.get(0);
        require("S0001".equals(first.getId()), "Unexpected first sample ID.");
        require(first.getJavaProgramming() == 95, "Unexpected Java score for first sample.");

        double averageJava = students.stream()
                .mapToInt(Student::getJavaProgramming)
                .average()
                .orElseThrow(() -> new IllegalStateException("No scores loaded."));
        require(averageJava > 80.0, "Average Java score should be above 80 in sample data.");

        System.out.println("Java grade manager smoke test passed.");
    }

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
