# Waste Classification Frontend

A modern, Material Design frontend for the Waste Classification API.

## Features

- **User Authentication**: Login and registration with JWT tokens
- **Image Upload**: Drag & drop or click to upload waste images
- **Real-time Classification**: Get instant waste type classification results
- **Classification History**: View all past classifications with pagination
- **Feedback System**: Provide feedback on classification accuracy
- **User Profile**: View and update profile, see statistics

## Setup

1. Make sure the Flask API backend is running on `http://localhost:5000`

2. Open `index.html` in a web browser, or use a local server:

   ```bash
   # Using Python
   cd client
   python -m http.server 8000

   # Using Node.js (if you have http-server installed)
   npx http-server -p 8000
   ```

3. Access the application at `http://localhost:8000`

## Configuration

To change the API base URL, edit `client/js/api.js`:

```javascript
const API_BASE_URL = "http://localhost:5000/api";
```

Change this to match your backend API URL.

## File Structure

```
client/
├── index.html          # Main HTML file
├── css/
│   ├── style.css      # Main Material Design styles
│   └── components.css # Component-specific styles
├── js/
│   ├── api.js         # API client
│   ├── auth.js        # Authentication logic
│   ├── app.js         # Main application
│   ├── utils.js       # Utility functions
│   └── components.js # UI components
└── README.md          # This file
```

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload Image**: Go to Dashboard and upload a waste image
3. **View Results**: See classification results with confidence scores
4. **History**: Check your classification history
5. **Profile**: View statistics and update your profile

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Notes

- Images are stored locally in the browser for preview
- JWT tokens are stored in localStorage
- The app uses Material Design principles for a modern UI
- Fully responsive for mobile and desktop
