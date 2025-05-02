system_prompt="You are a highly skilled software testing assistant with expertise in generating detailed and practical test cases for web and mobile applications. When generating test cases, consider both functional and non-functional scenarios, including edge cases, negative cases, and security aspects. Ensure the test cases are clear, structured, and can be easily used by QA engineers for manual or automated testing."

user_prompt =""" create all posible testing scenarios.
Title: Implement User Login Functionality
User Story: As an end-user, I want to be able to log into the website, So that I can access user-specific features and maintain the security of my personal data.
Acceptance Criteria:
User Interface:
The login page should have a clean and intuitive interface.
The page should include fields for username and password.
There should be a 'Login' button to submit the credentials.
A 'Forgot password' link should be provided.
An option to 'Register' should be available for new users.
Functionality:
The login should require a username (or email) and a password.
Input validation should be performed on the client side before submission:
The username/email field must not be empty.
The password field must not be empty and should adhere to security policies (minimum length, complexity).
Server-side validation should verify credentials against the database.
Users should receive an error message if the login fails.
Upon successful login, users should be redirected to their homepage/dashboard.
Sessions should timeout after a period of inactivity (e.g., 30 minutes).
Security:
Passwords must be stored securely in the database using a strong hashing algorithm.
The system should implement measures to prevent brute force attacks (e.g., account lockout after several failed login attempts).
All data exchanges should be encrypted using HTTPS.
Testing:
Unit tests must cover critical login functionalities.
Integration tests should ensure the login module works correctly with the user database and UI.
End-to-end tests should simulate the user login process and validate the overall workflow.
Documentation:
The login functionality should be documented clearly for future reference and updates.
Documentation should include details on the configuration of security settings and dependencies.
Additional Notes:
Ensure compatibility across all major browsers like Chrome, Firefox, Safari, and Edge.
Consider the implementation of multi-factor authentication (MFA) as a subsequent enhancement to increase security. """