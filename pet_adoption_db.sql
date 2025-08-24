CREATE DATABASE IF NOT EXISTS pet_adoption_db;
USE pet_adoption_db;

CREATE TABLE Pets (
    PetID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Species VARCHAR(50),
    Breed VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    ShelterID INT,
    Status ENUM('Available', 'Adopted') DEFAULT 'Available',
    ImageURL VARCHAR(255)
);

CREATE TABLE Adopters (
    AdopterID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    Address TEXT
);

CREATE TABLE Adoptions (
    AdoptionID INT AUTO_INCREMENT PRIMARY KEY,
    PetID INT,
    AdopterID INT,
    AdoptionDate DATE,
    Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (PetID) REFERENCES Pets(PetID),
    FOREIGN KEY (AdopterID) REFERENCES Adopters(AdopterID)
);

INSERT INTO Pets (Name, Species, Breed, Age, Gender, ShelterID, Status) VALUES
('Buddy', 'Dog', 'Golden Retriever', 3, 'Male', 1, 'Available'),
('Misty', 'Cat', 'Siamese', 2, 'Female', 1, 'Available'),
('Charlie', 'Dog', 'Labrador', 1, 'Male', 2, 'Adopted'),
('Bella', 'Dog', 'Labrador Retriever', 3, 'Female', 1, 'Available'),
('Milo', 'Cat', 'Siamese', 2, 'Male', 1, 'Available'),
('Rocky', 'Dog', 'German Shepherd', 4, 'Male', 2, 'Available'),
('Luna', 'Cat', 'Persian', 1, 'Female', 2, 'Available'),
('Cooper', 'Dog', 'Beagle', 2, 'Male', 3, 'Adopted');