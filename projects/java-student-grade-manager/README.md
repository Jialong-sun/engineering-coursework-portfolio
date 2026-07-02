# Java Student Grade Manager

A small Java Swing desktop application for loading student score records, showing them in a table, searching by name or ID, calculating course-level statistics, and exporting query results.

## What This Demonstrates

- Java Swing GUI development
- Table model (`DefaultTableModel`) and event-driven programming
- UTF-8 file parsing and object-oriented data modeling
- Immutable domain object design
- Basic input validation and malformed-row handling
- Sorting and summary statistics
- Maven-based build and JUnit test workflow

## Privacy Cleanup

The original coursework data contained real-looking names and student IDs. This portfolio version uses fully anonymized sample data under `data/student_scores_sample.csv`.

## Run

From this project directory:

```powershell
mvn test
mvn -DskipTests package
java -cp target/classes com.jialong.portfolio.grademanager.StudentSystem
```

## Test

The project includes JUnit tests for CSV loading and sample-data validation:

```powershell
mvn test
```

## Features

- Load tabular score data from CSV
- Display all records in a non-editable table
- Search by name or student ID
- Calculate max/min/average/median for each course
- Save query results to a UTF-8 tab-separated text file

## Possible Improvements

- Replace Swing with JavaFX or a web UI
- Add richer unit tests for statistics and UI-independent services
- Add CSV import/export menu controls
- Package as a runnable JAR
