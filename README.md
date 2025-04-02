
# Food N Table

## Overview
Food N Table is a web application that enables users to book tables and order food online from various restaurants. The platform aims to streamline dining experiences by offering a seamless reservation and food ordering system. Built with Django, it integrates Razorpay for secure payments and is deployed on PythonAnywhere.

## Features
- **Table Booking:** Users can book tables in advance at partnered restaurants.
- **Online Food Ordering:** Order food online and get it delivered or pick it up.
- **Restaurant Listings:** Browse and explore different restaurants and their menus.
- **Secure Payments:** Integrated Razorpay for seamless transactions.
- **User Authentication:** Sign up, login, and manage personal accounts.
- **Order Tracking:** Track the status of food orders in real-time.
- **Reviews & Ratings:** Users can review and rate restaurants.

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (optional frameworks like Bootstrap)
- **Database:** SQLite 
- **Payments:** Razorpay Integration
- **Hosting:** PythonAnywhere

## Installation
### Prerequisites
Ensure you have the following installed:
- Python (>=6.0)
- Virtualenv (optional but recommended)
- Git

### Steps to Set Up Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Codermvgr/FoodNTable.git
   cd FoodNTable
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Open the application in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Deployment
Food N Table is hosted on **PythonAnywhere**. You can access the live version here: [Food N Table Live](https://foodntable.pythonanywhere.com/)

## Demo Video
Watch the demo video of Food N Table here: [Demo Video](https://youtu.be/GL03nLPvuYo)

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes and push to GitHub.
4. Submit a Pull Request (PR).

## License
This project is licensed under the MIT License.

## Contact
For any queries, reach out at: [gullipallinagabhushan@gmail.com.com].

Happy coding! 🚀
