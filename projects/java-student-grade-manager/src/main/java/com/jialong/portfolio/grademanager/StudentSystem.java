package com.jialong.portfolio.grademanager;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.SwingUtilities;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableModel;
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class StudentSystem extends JFrame implements ActionListener {
    private static final String[] COLUMNS = {
            "ID", "Group", "Name", "Data Structures", "Operating Systems",
            "Software Engineering", "Java Programming", "Machine Learning"
    };
    private static final String[] COURSES = {
            "Data Structures", "Operating Systems", "Software Engineering",
            "Java Programming", "Machine Learning"
    };
    private static final String[] SEARCH_TYPES = {"Name", "ID"};

    private final DefaultTableModel model = new DefaultTableModel(COLUMNS, 0);
    private final JTable table = new JTable(model);
    private final JTextField searchField = new JTextField(18);
    private final JComboBox<String> courseBox = new JComboBox<>(COURSES);
    private final JComboBox<String> searchTypeBox = new JComboBox<>(SEARCH_TYPES);
    private final List<Student> students;

    public StudentSystem(String title) {
        super(title);
        StudentLoader loader = new StudentLoader();
        students = loader.readStudentInfo("data/student_scores_sample.csv");
        buildUi();
        showStudents(students);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new StudentSystem("Student Grade Manager"));
    }

    private void buildUi() {
        table.setDefaultEditor(Object.class, null);
        setLayout(new BorderLayout(8, 8));

        JPanel top = new JPanel(new GridLayout(2, 1, 6, 6));
        JPanel statsPanel = new JPanel();
        JButton statsButton = new JButton("Show Course Statistics");
        statsButton.setActionCommand("stats");
        statsButton.addActionListener(this);
        statsPanel.add(courseBox);
        statsPanel.add(statsButton);

        JPanel searchPanel = new JPanel();
        JButton searchButton = new JButton("Search");
        searchButton.setActionCommand("search");
        searchButton.addActionListener(this);
        JButton saveButton = new JButton("Save Results");
        saveButton.setActionCommand("save");
        saveButton.addActionListener(this);
        searchPanel.add(new JLabel("Keyword:"));
        searchPanel.add(searchField);
        searchPanel.add(searchTypeBox);
        searchPanel.add(searchButton);
        searchPanel.add(saveButton);

        top.add(statsPanel);
        top.add(searchPanel);
        add(top, BorderLayout.NORTH);
        add(new JScrollPane(table), BorderLayout.CENTER);

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(960, 640);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent event) {
        switch (event.getActionCommand()) {
            case "stats":
                showStatistics((String) courseBox.getSelectedItem());
                break;
            case "search":
                search();
                break;
            case "save":
                saveData(model);
                break;
            default:
                break;
        }
    }

    private void search() {
        String keyword = searchField.getText().trim().toLowerCase();
        if (keyword.isEmpty()) {
            showStudents(students);
            return;
        }

        String searchType = (String) searchTypeBox.getSelectedItem();
        List<Student> results = students.stream()
                .filter(s -> "Name".equals(searchType)
                        ? s.getName().toLowerCase().contains(keyword)
                        : s.getId().toLowerCase().contains(keyword))
                .collect(Collectors.toList());
        showStudents(results);
    }

    private void showStudents(List<Student> rows) {
        model.setRowCount(0);
        rows.stream()
                .sorted(Comparator.comparing(Student::getId))
                .forEach(s -> model.addRow(new Object[]{
                        s.getId(), s.getGroup(), s.getName(), s.getDataStructures(),
                        s.getOperatingSystems(), s.getSoftwareEngineering(),
                        s.getJavaProgramming(), s.getMachineLearning()
                }));
    }

    private void showStatistics(String course) {
        List<Integer> scores = students.stream()
                .map(s -> s.scoreFor(course))
                .sorted()
                .collect(Collectors.toCollection(ArrayList::new));
        if (scores.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No data loaded.");
            return;
        }
        int min = scores.get(0);
        int max = scores.get(scores.size() - 1);
        double average = scores.stream().mapToInt(Integer::intValue).average().orElse(0);
        double median = scores.size() % 2 == 0
                ? (scores.get(scores.size() / 2 - 1) + scores.get(scores.size() / 2)) / 2.0
                : scores.get(scores.size() / 2);
        JOptionPane.showMessageDialog(this, String.format(
                "%s%nMax: %d%nMin: %d%nAverage: %.2f%nMedian: %.2f",
                course, max, min, average, median
        ));
    }

    private void saveData(TableModel model) {
        if (model.getRowCount() == 0) {
            JOptionPane.showMessageDialog(this, "No rows to save.");
            return;
        }
        JFileChooser chooser = new JFileChooser();
        chooser.setSelectedFile(new File("query_results.tsv"));
        if (chooser.showSaveDialog(this) != JFileChooser.APPROVE_OPTION) {
            return;
        }
        try (BufferedWriter writer = Files.newBufferedWriter(
                chooser.getSelectedFile().toPath(),
                StandardCharsets.UTF_8
        )) {
            for (int col = 0; col < model.getColumnCount(); col++) {
                writer.write(model.getColumnName(col));
                writer.write(col == model.getColumnCount() - 1 ? System.lineSeparator() : "\t");
            }
            for (int row = 0; row < model.getRowCount(); row++) {
                for (int col = 0; col < model.getColumnCount(); col++) {
                    writer.write(String.valueOf(model.getValueAt(row, col)));
                    writer.write(col == model.getColumnCount() - 1 ? System.lineSeparator() : "\t");
                }
            }
            JOptionPane.showMessageDialog(this, "Saved: " + chooser.getSelectedFile().getAbsolutePath());
        } catch (IOException e) {
            JOptionPane.showMessageDialog(this, "Error saving file.");
        }
    }
}
