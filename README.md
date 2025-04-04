# Entertainment Hub 🎬

![Entertainment Hub Banner](https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1280&h=400&q=80)

A modern web application for discovering and tracking movies, TV shows, and anime. Built with Flask and powered by TMDB API.

## ✨ Features

- 🎭 Browse trending movies, TV shows, and anime
- 🔍 Advanced search with real-time suggestions
- ⭐ User favorites system
- 🌓 Dark/Light theme support
- 📱 Responsive design for all devices
- 🎨 Beautiful UI with smooth animations
- 🔐 User authentication with Firebase
- 🎥 Detailed media information and trailers

## 🖼️ Screenshots

<div style="display: flex; gap: 10px; margin-bottom: 20px;">
    <img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=400&h=300&q=80" alt="Home Page" width="400"/>
    <img src="https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=400&h=300&q=80" alt="Movie Details" width="400"/>
</div>

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Firebase account
- TMDB API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/entertainment-hub.git
cd entertainment-hub
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```env
TMDB_API_KEY=your_tmdb_api_key
FIREBASE_API_KEY=your_firebase_api_key
# Add other Firebase configuration variables
```

5. Run the application
```bash
python app.py
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth
- **API**: TMDB (The Movie Database)
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Custom CSS with Flexbox/Grid

## 🌟 Key Features Details

### Dynamic Content Loading
- Infinite scroll for continuous content browsing
- Real-time search suggestions
- Smooth loading animations

### User Experience
- Responsive design for all screen sizes
- Theme switching (Dark/Light mode)
- Toast notifications for user actions
- Intuitive navigation

### Movie/Show Details
- High-quality posters and backdrops
- Cast information
- Trailers and videos
- Similar content recommendations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for their extensive movie database
- [Firebase](https://firebase.google.com/) for authentication and database services
- [Unsplash](https://unsplash.com/) for beautiful images

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
