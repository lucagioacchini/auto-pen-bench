import requests
import time

# Set the base URL of your Bludit installation
base_url = "http://localhost:80"  # Adjust this if your port is different

# Step 1: Initial request to the install page
response = requests.get(f"{base_url}/install.php")
print("Accessed install page. Status code:", response.status_code)

# Step 2: Submit the installation form
install_data = {
    "timezone": "America/New_York",
    "password": "password",
    "email": "admin@example.com",
    "name": "Admin",
    "save": ""
}

response = requests.post(f"{base_url}/install.php", data=install_data)
print("Submitted installation form. Status code:", response.status_code)

# Step 3: Wait a bit for the installation to complete
time.sleep(5)

# Step 4: Check if the installation was successful
response = requests.get(base_url)
if "Login" in response.text:
    print("Bludit installation completed successfully!")
else:
    print("Something went wrong during the installation.")

print("You can now log in with:")
print("Username: admin")
print("Password: password")