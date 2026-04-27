-- Alter Forien keys
ALTER TABLE Clubs
  DROP FOREIGN KEY fk_clubs_faculty;

ALTER TABLE Meetings
  DROP FOREIGN KEY fk_meetings_club;

ALTER TABLE Participation
  DROP FOREIGN KEY fk_participation_club;

ALTER TABLE Participation
  DROP FOREIGN KEY fk_participation_student;

DROP TABLE IF EXISTS Participation;
DROP TABLE IF EXISTS Meetings;
DROP TABLE IF EXISTS Clubs;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Faculty;

CREATE TABLE Faculty (
    Faculty_ID INT AUTO_INCREMENT PRIMARY KEY,
    Faculty_Name VARCHAR(70) NOT NULL UNIQUE
);

CREATE TABLE Student (
    Student_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_Name VARCHAR(70) NOT NULL
);

CREATE TABLE Clubs (
    Club_Name VARCHAR(70) NOT NULL,
    Curr_Year YEAR NOT NULL,
    Faculty_ID INT NOT NULL,
    Annual_Expenses DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Annual_Budget DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (Club_Name, Curr_Year),
    CONSTRAINT fk_clubs_faculty
        FOREIGN KEY (Faculty_ID) REFERENCES Faculty(Faculty_ID)
        ON UPDATE CASCADE
);

CREATE TABLE Meetings (
    Meeting_ID INT AUTO_INCREMENT PRIMARY KEY,
    Club_Name VARCHAR(70) NOT NULL,
    Curr_Year YEAR NOT NULL,
    Meeting_Date DATE NOT NULL,
    Meeting_Time TIME NOT NULL,
    Meeting_Location VARCHAR(100) NOT NULL,
    Meeting_Description VARCHAR(255),
    CONSTRAINT fk_meetings_club
        FOREIGN KEY (Club_Name, Curr_Year) REFERENCES Clubs(Club_Name, Curr_Year)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_room_timeslot
        UNIQUE (Meeting_Date, Meeting_Time, Meeting_Location),
    CONSTRAINT uq_club_timeslot
        UNIQUE (Club_Name, Curr_Year, Meeting_Date, Meeting_Time)
);

CREATE TABLE Participation (
    Student_ID INT NOT NULL,
    Club_Name VARCHAR(70) NOT NULL,
    Curr_Year YEAR NOT NULL,
    PRIMARY KEY (Student_ID, Club_Name, Curr_Year),
    CONSTRAINT fk_participation_student
        FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_participation_club
        FOREIGN KEY (Club_Name, Curr_Year) REFERENCES Clubs(Club_Name, Curr_Year)
        ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Faculty (Faculty_Name) VALUES
('Ms. Carter'),
('Mr. Nguyen'),
('Dr. Patel');

INSERT INTO Student (Student_Name) VALUES
('James Parker'),
('Ramiru Abernathy'),
('Parker Jenkins'),
('Jacky Lin'),
('Aiden Smith'),
('Bella Johnson'),
('Carlos Garcia'),
('Diana Lee'),
('Ethan Brown');

INSERT INTO Clubs (Club_Name, Curr_Year, Faculty_ID, Annual_Expenses, Annual_Budget) VALUES
('Band', 2026, 1, 1200.00, 3000.00),
('MathCounts', 2026, 2, 450.00, 1500.00),
('Speech', 2026, 3, 700.00, 2000.00),
('Choir', 2026, 1, 300.00, 1200.00);

INSERT INTO Meetings (Club_Name, Curr_Year, Meeting_Date, Meeting_Time, Meeting_Location, Meeting_Description) VALUES
('Band', 2026, '2026-04-28', '15:30:00', 'Music Room', 'Weekly rehearsal'),
('MathCounts', 2026, '2026-04-28', '15:30:00', 'Room 101', 'Competition practice'),
('Speech', 2026, '2026-04-29', '16:00:00', 'Room 202', 'Speech practice'),
('Choir', 2026, '2026-04-30', '15:30:00', 'Music Room', 'Choir rehearsal');

INSERT INTO Participation (Student_ID, Club_Name, Curr_Year) VALUES
(1, 'Band', 2026),
(2, 'Band', 2026),
(2, 'MathCounts', 2026),
(3, 'MathCounts', 2026),
(4, 'Speech', 2026),
(5, 'Choir', 2026);
