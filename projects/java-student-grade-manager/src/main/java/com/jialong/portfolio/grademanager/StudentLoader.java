package com.jialong.portfolio.grademanager;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class StudentLoader {
    private static final int EXPECTED_FIELDS = 8;

    public List<Student> readStudentInfo(String filename) {
        List<Student> students = new ArrayList<>();
        Path path = Paths.get(filename);
        if (!Files.exists(path)) {
            System.err.println("Data file not found: " + filename);
            return students;
        }

        try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            String line;
            int lineNumber = 0;
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                if (lineNumber == 1 || line.trim().isEmpty()) {
                    continue;
                }
                try {
                    students.add(parseStudentLine(line, lineNumber));
                } catch (IllegalArgumentException ex) {
                    System.err.println("Skipping row " + lineNumber + ": " + ex.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println("Failed to read data file: " + e.getMessage());
        }
        return students;
    }

    private Student parseStudentLine(String line, int lineNumber) {
        String[] fields = line.split(",", -1);
        if (fields.length != EXPECTED_FIELDS) {
            throw new IllegalArgumentException(
                    "expected " + EXPECTED_FIELDS + " fields, got " + fields.length
            );
        }

        try {
            return new Student(
                    fields[0].trim(),
                    fields[1].trim(),
                    fields[2].trim(),
                    parseScore(fields[3]),
                    parseScore(fields[4]),
                    parseScore(fields[5]),
                    parseScore(fields[6]),
                    parseScore(fields[7])
            );
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("invalid score on line " + lineNumber);
        }
    }

    private int parseScore(String value) {
        int score = Integer.parseInt(value.trim());
        if (score < 0 || score > 100) {
            throw new NumberFormatException("score out of range: " + score);
        }
        return score;
    }
}
