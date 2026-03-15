# Shaadi Matrimonial App

A modern matrimonial platform built with Frappe framework and Vue.js, featuring swipe-based matching, real-time messaging, and comprehensive profile management.

## 🌟 Features

### Core Functionality
- **Swipe-Based Matching**: Tinder-like interface for finding matches
- **Mutual Matches**: Automatic detection when both users like each other
- **Real-Time Messaging**: Live chat with matched profiles
- **Advanced Search**: Filter by preferences, location, education, etc.
- **Profile Management**: Complete member profiles with photos and details
- **Partner Preferences**: Set and manage matching criteria
- **Interest System**: Send and receive interest notifications
- **Shortlist**: Save favorite profiles for later

### Technical Features
- **Gender-Based Matching**: Smart algorithm based on partner preferences
- **Privacy Controls**: Block/unblock members, manage visibility
- **Subscription Management**: Premium features with subscription plans
- **Responsive Design**: Works seamlessly on all devices
- **Real-Time Updates**: Live notifications and status updates

## 🛠 Tech Stack

### Backend
- **Framework**: Frappe (Python)
- **Database**: MariaDB/PostgreSQL
- **API**: RESTful endpoints with Frappe framework
- **Real-Time**: WebSocket support

### Frontend
- **Framework**: Vue 3 + Vite
- **Styling**: Tailwind CSS
- **UI Components**: Frappe UI
- **State Management**: Vue 3 Composition API
- **Icons**: Feather Icons

### DevOps
- **CI/CD**: GitHub Actions
- **Branching**: Git Flow (dev → main)
- **Testing**: Unit tests and integration tests
- **Security**: Automated security scanning

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Frappe Bench

### Setup
```bash
# Clone the repository
git clone https://github.com/amitascra/shaadi-frappe-app.git
cd shaadi-frappe-app

# Setup Frappe bench
bench init --skip-assets
bench get-app https://github.com/amitascra/shaadi-frappe-app.git

# Install dependencies
bench setup requirements --dev
bench new-site shaadi.localhost
bench --site shaadi.localhost install-app shaadi

# Build frontend
cd apps/shaadi/shaadi_ui
npm install
npm run build

# Start development
bench start
```

## 🚀 Development

### Branching Strategy
- **main**: Production-ready code
- **dev**: Development branch
- **feature/***: Feature branches
- **hotfix/***: Critical fixes

### Workflow
1. Create feature branch from `dev`
2. Develop and test locally
3. Push to feature branch
4. Create PR to `dev`
5. Merge to `dev` triggers auto-merge to `main`
6. `main` deploys to production

### Local Development
```bash
# Switch to dev branch
git checkout dev

# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

## 🔄 CI/CD Pipeline

### Automated Tests
- **Unit Tests**: Frontend and backend components
- **Integration Tests**: API endpoints and database operations
- **Security Scans**: Code vulnerability detection
- **Build Tests**: Frontend build verification

### Deployment
- **Development**: Auto-deploy on `dev` branch push
- **Production**: Auto-deploy on `main` branch push
- **Rollback**: Automatic rollback on failed deployment

## 📱 Access Points

### Frontend URLs
- **Home**: `http://localhost:8000`
- **Login**: `http://localhost:8000/signin`
- **Dashboard**: `http://localhost:8000/dashboard`
- **Browse**: `http://localhost:8000/browse`
- **Matches**: `http://localhost:8000/matches`

### Backend APIs
- **Authentication**: `/api/method/shaadi.shaadi.api.auth.*`
- **Profiles**: `/api/method/shaadi.shaadi.api.profile.*`
- **Matching**: `/api/method/shaadi.shaadi.api.matchmaking.*`
- **Messaging**: `/api/method/shaadi.shaadi.api.messaging.*`

## 🎨 UI/UX Features

### Theme
- **Color Scheme**: Pink/Purple gradient theme
- **Responsive**: Mobile-first design approach
- **Accessibility**: WCAG 2.1 compliant
- **Performance**: Optimized for fast loading

### Components
- **Swipe Cards**: Interactive profile cards with swipe gestures
- **Match Modal**: Celebration modal for mutual matches
- **Real-Time Chat**: Live messaging interface
- **Profile Cards**: Comprehensive profile display
- **Filter Panel**: Advanced search and filtering

## 🔧 Configuration

### Environment Variables
```env
# Frappe Configuration
FRAPPE_SITE=shaadi.localhost
FRAPPE_DB_HOST=localhost
FRAPPE_DB_PORT=3306

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### App Settings
- **Role Management**: Matrimonial Member, Premium Member, Admin
- **Permissions**: Granular access control
- **Notifications**: Email and in-app notifications
- **Privacy Settings**: Profile visibility and data protection

## 📊 Analytics & Monitoring

### Metrics
- **User Engagement**: Profile views, swipe actions, messages
- **Match Success**: Mutual matches, conversation rates
- **Performance**: Page load times, API response times
- **Security**: Login attempts, failed authentications

### Monitoring
- **Error Tracking**: Comprehensive error logging
- **Performance Monitoring**: Real-time performance metrics
- **Uptime Monitoring**: Service availability tracking
- **User Analytics**: Behavior and engagement analytics

## 🤝 Contributing

### Guidelines
1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Create pull requests with clear descriptions
5. Ensure all tests pass before merging

### Code Style
- **Python**: PEP 8 compliant
- **JavaScript**: ESLint + Prettier
- **Vue.js**: Vue 3 Composition API
- **CSS**: Tailwind CSS utility classes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Amit Kumar**
- **Portfolio**: https://resume.amitkumar.live/
- **GitHub**: https://github.com/amitascra
- **Email**: [Contact via portfolio]

## 🙏 Acknowledgments

- **Frappe Framework**: Powerful backend framework
- **Vue.js**: Progressive JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Feather Icons**: Beautiful icon set

---

**Made with love ❤️ by Amit Kumar**
