package com.jialong.portfolio.grademanager;

public final class Student {
    private final String id;
    private final String group;
    private final String name;
    private final int dataStructures;
    private final int operatingSystems;
    private final int softwareEngineering;
    private final int javaProgramming;
    private final int machineLearning;

    public Student(
            String id,
            String group,
            String name,
            int dataStructures,
            int operatingSystems,
            int softwareEngineering,
            int javaProgramming,
            int machineLearning
    ) {
        this.id = id;
        this.group = group;
        this.name = name;
        this.dataStructures = dataStructures;
        this.operatingSystems = operatingSystems;
        this.softwareEngineering = softwareEngineering;
        this.javaProgramming = javaProgramming;
        this.machineLearning = machineLearning;
    }

    public String getId() {
        return id;
    }

    public String getGroup() {
        return group;
    }

    public String getName() {
        return name;
    }

    public int getDataStructures() {
        return dataStructures;
    }

    public int getOperatingSystems() {
        return operatingSystems;
    }

    public int getSoftwareEngineering() {
        return softwareEngineering;
    }

    public int getJavaProgramming() {
        return javaProgramming;
    }

    public int getMachineLearning() {
        return machineLearning;
    }

    public int scoreFor(String course) {
        switch (course) {
            case "Data Structures":
                return dataStructures;
            case "Operating Systems":
                return operatingSystems;
            case "Software Engineering":
                return softwareEngineering;
            case "Java Programming":
                return javaProgramming;
            case "Machine Learning":
                return machineLearning;
            default:
                throw new IllegalArgumentException("Unknown course: " + course);
        }
    }
}
