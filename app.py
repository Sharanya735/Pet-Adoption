from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import date
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  
            database='pet_adoption_db'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_pets')
def view_pets():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return render_template('view_pets.html', pets=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pets WHERE Status = 'Available'")
        pets = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('view_pets.html', pets=pets)
    except Exception as e:
        flash(f'Error loading pets: {str(e)}', 'error')
        return render_template('view_pets.html', pets=[])

@app.route('/adopt/<int:pet_id>', methods=['GET', 'POST'])
def adopt(pet_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return redirect(url_for('view_pets'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get pet details
        cursor.execute("SELECT * FROM Pets WHERE PetID = %s AND Status = 'Available'", (pet_id,))
        pet = cursor.fetchone()
        
        if not pet:
            flash('Pet not found or already adopted.', 'error')
            return redirect(url_for('view_pets'))
        
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            
            # Validate form data
            if not all([name, email, phone, address]):
                flash('Please fill in all fields.', 'error')
                return render_template('adopt_form.html', pet=pet)
            
            # Insert adopter
            cursor.execute("INSERT INTO Adopters (FullName, Email, Phone, Address) VALUES (%s, %s, %s, %s)",
                           (name, email, phone, address))
            adopter_id = cursor.lastrowid
            
            # Insert adoption record
            cursor.execute("""
            INSERT INTO Adoptions (PetID, AdopterID, AdoptionDate, Status)
            VALUES (%s, %s, %s, %s)
            """, (pet_id, adopter_id, date.today(), 'Pending'))
            
            # Update pet status
            cursor.execute("UPDATE Pets SET Status = 'Adopted' WHERE PetID = %s", (pet_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Adoption request submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('view_pets'))
        
        cursor.close()
        conn.close()
        return render_template('adopt_form.html', pet=pet)
        
    except Exception as e:
        flash(f'Error processing adoption: {str(e)}', 'error')
        return redirect(url_for('view_pets'))

@app.route('/admin_dashboard')
def admin_dashboard():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return render_template('admin_dashboard.html', pets=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pets ORDER BY PetID DESC")
        pets = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_dashboard.html', pets=pets)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('admin_dashboard.html', pets=[])

@app.route('/adoption_requests')
def adoption_requests():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return render_template('adoption_requests.html', requests=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT A.AdoptionID, P.Name AS PetName, U.FullName AS AdopterName, 
                   A.AdoptionDate, A.Status, U.Email, U.Phone
            FROM Adoptions A
            JOIN Pets P ON A.PetID = P.PetID
            JOIN Adopters U ON A.AdopterID = U.AdopterID
            ORDER BY A.AdoptionDate DESC
        """)
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('adoption_requests.html', requests=requests)
    except Exception as e:
        flash(f'Error loading adoption requests: {str(e)}', 'error')
        return render_template('adoption_requests.html', requests=[])

@app.route('/update_adoption_status/<int:adoption_id>/<status>')
def update_adoption_status(adoption_id, status):
    if status not in ['Approved', 'Rejected']:
        flash('Invalid status.', 'error')
        return redirect(url_for('adoption_requests'))
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return redirect(url_for('adoption_requests'))
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Adoptions SET Status = %s WHERE AdoptionID = %s", (status, adoption_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash(f'Adoption request {status.lower()} successfully.', 'success')
        return redirect(url_for('adoption_requests'))
    except Exception as e:
        flash(f'Error updating status: {str(e)}', 'error')
        return redirect(url_for('adoption_requests'))

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        try:
            data = (
                request.form['name'],
                request.form['species'],
                request.form['breed'],
                int(request.form['age']),
                request.form['gender'],
                int(request.form['shelter_id']),
                request.form['status'],
                request.form.get('image_url', '')
            )
            
            conn = get_db_connection()
            if not conn:
                flash('Database connection error. Please try again later.', 'error')
                return render_template('add_pet.html')
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Pets (Name, Species, Breed, Age, Gender, ShelterID, Status, ImageURL) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Pet added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except ValueError:
            flash('Please enter valid numbers for age and shelter ID.', 'error')
        except Exception as e:
            flash(f'Error adding pet: {str(e)}', 'error')
    
    return render_template('add_pet.html')

@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            data = (
                request.form['name'],
                request.form['species'],
                request.form['breed'],
                int(request.form['age']),
                request.form['gender'],
                int(request.form['shelter_id']),
                request.form['status'],
                request.form.get('image_url', ''),
                pet_id
            )
            
            cursor.execute("""
                UPDATE Pets 
                SET Name=%s, Species=%s, Breed=%s, Age=%s, Gender=%s, ShelterID=%s, Status=%s, ImageURL=%s 
                WHERE PetID=%s
            """, data)
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Pet updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        
        cursor.execute("SELECT * FROM Pets WHERE PetID = %s", (pet_id,))
        pet = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not pet:
            flash('Pet not found.', 'error')
            return redirect(url_for('admin_dashboard'))
        
        return render_template('edit_pet.html', pet=pet)
        
    except ValueError:
        flash('Please enter valid numbers for age and shelter ID.', 'error')
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        flash(f'Error editing pet: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/delete_pet/<int:pet_id>')
def delete_pet(pet_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please try again later.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        cursor = conn.cursor()
        
        # Check if pet has any adoption records
        cursor.execute("SELECT COUNT(*) FROM Adoptions WHERE PetID = %s", (pet_id,))
        adoption_count = cursor.fetchone()[0]
        
        if adoption_count > 0:
            flash('Cannot delete pet with existing adoption records.', 'error')
            return redirect(url_for('admin_dashboard'))
        
        cursor.execute("DELETE FROM Pets WHERE PetID = %s", (pet_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Pet deleted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        flash(f'Error deleting pet: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
