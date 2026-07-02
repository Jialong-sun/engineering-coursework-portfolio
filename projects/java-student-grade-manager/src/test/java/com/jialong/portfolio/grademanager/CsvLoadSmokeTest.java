package com.jialong.portfolio.grademanager;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CsvLoadSmokeTest {
    @Test
    void sampleDatasetIsLoadable() {
        List<Student> students = new StudentLoader().readStudentInfo("data/student_scores_sample.csv");

        assertEquals(10, students.size());
        assertEquals("S0001", students.get(0).getId());
        assertEquals(95, students.get(0).getJavaProgramming());

        double averageJava = students.stream()
                .mapToInt(Student::getJavaProgramming)
                .average()
                .orElseThrow();

        assertTrue(averageJava > 80.0);
    }
}
