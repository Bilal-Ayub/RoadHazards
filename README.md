# Road Hazard reporter⚠️



## Features

1. **User Authentication:**
   - User registration and login functionality.
   - Password validation 
2. **Pothole Reporting:**
   - Users can report potholes by providing a longitude and latitude, a description and uploading images.
   - Pothole reports are stored in the database
3. **Map View:**
   - Users can view reported potholes on a map.
   - markers show reports 
   - markers can be clicked to show individual details


## Prerequisites

- See requirements.txt

## Setup Instructions

1. **Clone the repository:**
   

2. **Create a virtual environment:**
   In the terminal, navigate to the project directory and run the following command to create a virtual environment named `my_env`:
   
   ```sh
   python -m venv my_env
   ```

3. **Activate the virtual environment:**
   Run the following command to activate the virtual environment:
   
   ```sh
   my_env\Scripts\activate
   ```

4. **Install the required packages:**
   With the virtual environment activated, run the following command to install the required packages listed in `requirements.txt`:
   
   ```sh
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the project root directory and add the necessary environment variables. For example:
   
   ```plaintext
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

6. **Apply database migrations:**
   Run the following command to apply the database migrations:
   
   ```sh
   python manage.py migrate
   ```

7. **Create a superuser:**
   Run the following command to create a superuser for accessing the Django admin interface:
   
   ```sh
   python manage.py createsuperuser
   ```

8. **Run the development server:**
   Start the Django development server by running the following command:
   
   ```sh
   python manage.py runserver
   ```

9. **Access the application:**
   Go to the link given by the command runserver
