-- Drop old tables
DROP TABLE IF EXISTS FACULTY;
DROP TABLE IF EXISTS STUDENT;
DROP TABLE IF EXISTS CLUBS;
DROP TABLE IF EXISTS MEETINGS;
DROP TABLE IF EXISTS PARTICIPATION;

-- Create Faculty Table
CREATE TABLE FACULTY (
    Faculty_ID INT PRIMARY KEY AUTO_INCREMENT,
    Faculty_Name VARCHAR(70) NOT NULL
);

-- Create Student Table
CREATE TABLE STUDENT (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_Name VARCHAR(70) NOT NULL
);

-- Create Clubs Table
CREATE TABLE CLUBS (
    Club_Name VARCHAR(70) ,
    Faculty_ID INT,
    Annual_Expenses DECIMAL(10, 2),
    Annual_Budget DECIMAL(10, 2),
    Curr_Year YEAR,

    PRIMARY KEY (Club_Name, Curr_Year),

    -- Create foreign key constraint on faculty_id
    CONSTRAINT FALCULTY_FK FOREIGN KEY (Faculty_ID) REFERENCES FACULTY(Faculty_ID)
);

-- Create Meetings Table
CREATE TABLE MEETINGS (
    MEETING_ID INT PRIMARY KEY AUTO_INCREMENT,
    Club_Name VARCHAR(70),
    Meeting_Date DATE,
    Meeting_Time TIME,
    Meeting_Location VARCHAR(100),
    MEETING_DESCRIPTION VARCHAR(255),

    -- Create foreign key constraint on club_name
    CONSTRAINT CLUBS_FK FOREIGN KEY (Club_Name) REFERENCES CLUBS(Club_Name)

);

-- Create the student club participation table
CREATE TABLE PARTICIPATION (
    Student_ID INT NOT NULL,
    Club_Name VARCHAR(70) NOT NULL,

    -- Composite Primary key on Student_ID and Club_Name
    PRIMARY KEY (Student_ID, Club_Name),

    -- Create foreign key constraints on Student_ID and Club_Name
    CONSTRAINT STUDENT_FK FOREIGN KEY (Student_ID) REFERENCES STUDENT(Student_ID),
    CONSTRAINT CLUBS_FK FOREIGN KEY (Club_Name) REFERENCES CLUBS(Club_Name)
);

-- Insert sample data
INSERT INTO FACULTY (Faculty_Name) VALUES
('Mr. Jones'),
('Ms. Smith'),
('Dr. Brown');

INSERT INTO STUDENT(Student_Name) VALUES
('James Parker'),
('Ramiru Abernathy'),
('Parker Jenkins'),
('Jackie Lin');

INSERT INTO CLUBS(Club_Name, Faculty_ID, Annual_Expenses, Annual_Budget, Curr_Year) VALUES
('Chess Club', 1, 500.00, 1000.00, 2026),
('Chess Club', 1, 800.00, 2000.00, 2025),
('Robotics Club', 2, 1500.00, 2000.00, 2026),
('Drama Club', 3, 800.00, 1200.00, 2026);

INSERT INTO MEETINGS(Club_Name, Meeting_Date, Meeting_Time, Meeting_Location, MEETING_DESCRIPTION) VALUES
('Chess Club', '2026-09-15', '18:00:00', 'Room 101', 'Weekly chess practice and strategy discussion.'),
('Chess Club', '2026-09-16', '14:00:00', 'William T Young Library', 'State tournament.'),
('Robotics Club', '2026-09-20', '17:00:00', 'Lab 202', 'Introduction to robotics and project planning.'),
('Drama Club', '2026-09-25', '19:00:00', 'Auditorium', 'Rehearsal for the upcoming school play.');

INSERT INTO PARTICIPATION(Student_ID, Club_Name) VALUES
(1, 'Chess Club'),
(2, 'Chess Club'),
(2, 'Robotics Club'),
(3, 'Robotics Club'),
(4, 'Drama Club');