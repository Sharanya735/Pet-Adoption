# 🐾 Pet Adoption Portal

A beautiful and fully functional pet adoption website built with Flask and MySQL. This application allows users to browse available pets, submit adoption requests, and provides an admin dashboard for managing pets and adoption requests.

## ✨ Features

### For Users:
- 🏠 **Beautiful Home Page** - Modern, responsive design with gradient backgrounds
- 🐕 **Browse Available Pets** - View all pets available for adoption with detailed information
- ❤️ **Adoption Process** - Easy-to-use adoption form with validation
- 📱 **Mobile Responsive** - Works perfectly on all devices

### For Administrators:
- 📋 **Admin Dashboard** - Manage all pets in the system
- ➕ **Add New Pets** - Add pets with detailed information
- ✏️ **Edit Pet Details** - Update pet information easily
- 🗑️ **Delete Pets** - Remove pets (with safety checks)
- 📋 **Adoption Requests** - View and manage all adoption requests
- ✅ **Approve/Reject** - Approve or reject adoption requests
- 🔔 **Flash Messages** - Real-time feedback for all actions

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Responsive Design**: Mobile-first approach

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.7+** installed on your system
2. **MySQL Server** installed and running
3. **pip** (Python package installer)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Pet-Adoption
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

1. **Start MySQL Server**
2. **Create Database and Tables**:
   ```bash
   mysql -u root -p < pet_adoption_db.sql
   ```
   
   Or manually run the SQL commands in your MySQL client:
   ```sql
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
   ```

### 4. Configure Database Connection

Edit the database connection settings in `app.py` if needed:
```python
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',          # Change to your MySQL username
        password='root',      # Change to your MySQL password
        database='pet_adoption_db'
    )
    return conn
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 📁 Project Structure

```
Pet-Adoption/
├── app.py                 # Main Flask application
├── pet_adoption_db.sql    # Database schema and sample data
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── styles.css        # Additional CSS styles
└── templates/
    ├── home.html         # Home page
    ├── view_pets.html    # Available pets page
    ├── adopt_form.html   # Adoption form
    ├── admin_dashboard.html  # Admin dashboard
    ├── adoption_requests.html # Adoption requests management
    ├── add_pet.html      # Add new pet form
    └── edit_pet.html     # Edit pet form
```

## 🎯 How to Use

### For Users:
1. **Visit the Home Page** - Navigate to the main page
2. **Browse Pets** - Click "View Available Pets" to see all available pets
3. **Adopt a Pet** - Click "Adopt Me!" on any pet you're interested in
4. **Fill Form** - Complete the adoption form with your details
5. **Submit Request** - Your adoption request will be submitted for review

### For Administrators:
1. **Access Admin Dashboard** - Click "Admin Dashboard" from the home page
2. **Manage Pets** - Add, edit, or delete pets as needed
3. **View Requests** - Click "View Adoption Requests" to see all requests
4. **Approve/Reject** - Approve or reject adoption requests
5. **Monitor Status** - Track the status of all pets and adoptions

## 🔧 Features Explained

### Flash Messages
- **Success Messages**: Green notifications for successful actions
- **Error Messages**: Red notifications for errors or warnings
- **Auto-hide**: Messages automatically disappear after 5 seconds

### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Tablet Support**: Works great on tablets
- **Desktop Experience**: Enhanced experience on larger screens

### Security Features
- **Input Validation**: All form inputs are validated
- **SQL Injection Protection**: Parameterized queries prevent SQL injection
- **Error Handling**: Graceful error handling throughout the application

### Database Features
- **Foreign Key Constraints**: Maintains data integrity
- **Status Tracking**: Tracks adoption request status
- **Audit Trail**: Records all adoption activities

## 🐛 Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Ensure MySQL server is running
   - Check username and password in `app.py`
   - Verify database exists

2. **Port Already in Use**
   - Change the port in `app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```

3. **Module Not Found Errors**
   - Install dependencies: `pip install -r requirements.txt`

4. **Permission Errors**
   - Ensure you have write permissions in the project directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- MySQL for the reliable database system
- All contributors who help improve this project

---

**Made with ❤️ for pet lovers everywhere! 🐾**
