# 🌱 EcoSort – Premium AI Waste Classification

**Sort smarter. Waste less.**

EcoSort is a premium environmental technology product that uses AI to identify everyday waste and guide you toward the right disposal method. Make a real difference, one item at a time.

---

## ✨ Premium Environmental Design

EcoSort features a completely redesigned, premium user interface inspired by environmental editorial websites. The design emphasizes:

- **Minimal aesthetic** with warm off-white backgrounds and sage green accents
- **Editorial typography** with large, readable hierarchy (90px hero headlines)
- **Generous whitespace** for breathing room and clarity
- **Smooth animations** for subtle, premium interactions
- **Premium buttons** with rounded pill shapes and smooth hover effects
- **Professional color palette**: Deep forest green (#1b4d2e), sage green (#6b9b7e), warm ivory (#f5f3f0)
- **Full responsive design** optimized for mobile, tablet, and desktop

---

## 🎯 What EcoSort Does

EcoSort helps you make better waste-disposal decisions. Take a photo of any waste item, and EcoSort will:

- 🔍 **Identify** what the item is using AI vision
- 🏷️ **Classify** which waste category it belongs to
- 📋 **Guide** you on how to dispose of it properly
- ⚠️ **Warn** about potential safety hazards
- 🌍 **Localize** advice based on your region
- ♻️ **Suggest** eco-friendly alternatives
- 🔄 **Recommend** reuse options when applicable

---

## 🎨 UI Components

The redesigned interface includes:

- **Navigation Bar** - Sticky header with logo, navigation links, and CTA
- **Hero Section** - Editorial headline "Sort smarter. Waste less." with key statistics
- **Animated Marquee** - Scrolling sustainability message
- **How It Works** - Three-step editorial process (Upload, Analyze, Sort)
- **AI Scanner** - Large drop zone for waste images with region selector
- **Analyzing State** - Beautiful animated loading state
- **Classification Result** - Detailed waste analysis with visual hierarchy
- **Waste Categories** - Six category cards with descriptions
- **Impact Section** - Dark green statistics section showing scan metrics
- **Why EcoSort** - Four-column benefit section
- **Final CTA** - Editorial call-to-action section
- **Footer** - Minimal footer with links and copyright

---

## ⚡ Features

### MVP Features (Implemented)

- ✅ Premium UI/UX redesign with editorial aesthetic
- ✅ Image upload support with elegant drop zone
- ✅ Vision-based waste identification using Groq API
- ✅ Six waste categories: Recyclable, Organic, Hazardous, Electronic, General, Reusable
- ✅ Confidence-aware results (High, Medium, Low)
- ✅ Safety warning system
- ✅ Eco-friendly tips
- ✅ Reuse suggestions
- ✅ Region selector with local guidance (Global, USA, Pakistan, UK, Canada)
- ✅ Disposal step-by-step instructions
- ✅ Beautiful result card with numbered steps
- ✅ Full responsive design (mobile-first)
- ✅ Smooth animations and transitions
- ✅ Accessible color contrast and keyboard navigation
- ✅ Error handling and graceful API failures

### Future Features

- 🔄 Scan history with user accounts
- 📊 Environmental impact dashboard
- 🌐 Multilingual support (Urdu, Spanish, French, etc.)
- 👍 User feedback system
- 🚩 Flag incorrect results for review
- 📍 Nearby recycling center locator
- 🎮 Gamification (badges, streaks, etc.)
- 🤖 Admin dashboard for review queue
- 📱 Native mobile app
- 🏢 Municipal integrations

---

## 🛠️ Technology Stack

- **Backend**: Python 3.8+
- **Frontend**: Streamlit 1.57+
- **AI/Vision**: Groq API with vision-capable LLM
- **Styling**: Custom CSS with modern design tokens
- **Image Processing**: Pillow
- **HTTP**: Requests
- **Configuration**: python-dotenv
- **Typography**: Inter (modern, clean sans-serif from Google Fonts)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Groq API key (get one at https://console.groq.com)
- A current vision-capable Groq model

### Installation

1. **Clone the repository** (or download the project)
   ```bash
   git clone https://github.com/your-username/ecosort-ai.git
   cd EcoSort-AI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   GROQ_MODEL=llama-2-vision-13b
   ```
   
   > ⚠️ **Important**: Never commit `.env` to GitHub. It contains sensitive credentials.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

---

## 🎨 Design System & Premium Aesthetic

EcoSort's redesigned UI features a professional environmental aesthetic inspired by premium sustainability brands:

### Color Palette
- **Background**: Warm off-white/ivory (#f5f3f0)
- **Primary**: Deep forest green (#1b4d2e)
- **Secondary**: Sage green (#6b9b7e)
- **Accent**: Soft sage/lime (#a8d5ba)
- **Text**: Near-black (#1a1a1a)
- **Muted Text**: Gray-green (#6b7565)
- **Borders**: Subtle gray-green (#d9d6d0)

### Typography
- **Font Family**: Inter (modern, clean geometric sans-serif)
- **Hero Headline**: 90px bold with -2px letter-spacing
- **Section Headlines**: 56px bold
- **Body**: 16-18px with 1.6 line-height
- **Strong visual hierarchy** for improved readability

### Design Elements
- **Pill-shaped buttons** with smooth hover transitions
- **Subtle borders** on cards and surfaces
- **Generous whitespace** for premium feel
- **Smooth animations** (fade-in, pulse, shimmer)
- **Responsive grid layouts** that adapt to all screen sizes
- **Accessible color contrast** (WCAG AA compliant)

### Responsive Breakpoints
- **Desktop**: Full-width with generous padding
- **Tablet**: Optimized 2-column layouts
- **Mobile**: Single-column stacked layout with adjusted typography

---

## 📖 How to Use

1. **Upload an Image** — Click on the drop zone or browse to upload a waste item photo
2. **Select Your Region** — Choose your location for region-specific disposal guidance
3. **Analyze** — Click the "🔍 Analyze Waste" button
4. **Review Results** — See:
   - What the item is
   - Which waste category it belongs to
   - How confident the AI is
   - Step-by-step disposal instructions
   - Safety warnings (if applicable)
   - Eco-friendly tips
   - Reuse suggestions
   - Region-specific guidance
5. **Scan Again** — Click "🔄 Scan Another Item" to analyze more waste

---

## 🧪 Demo & Testing

### Test Items for Demo

Try these items to see how EcoSort works:

#### ✅ Test 1: Plastic Bottle (Recyclable)
- **Expected Category**: Recyclable
- **Expected Confidence**: High
- **Expected Tip**: Rinse before recycling, consider reusing or refilling

#### ✅ Test 2: Banana Peel (Organic)
- **Expected Category**: Organic/Compostable
- **Expected Confidence**: High
- **Expected Tip**: Add to compost or home composting

#### ⚠️ Test 3: Battery (Hazardous)
- **Expected Category**: Hazardous or Electronic Waste
- **Expected Confidence**: High
- **Expected Warning**: Do not place in regular recycling
- **Expected Tip**: Take to hazardous waste facility

---

## ⚙️ Configuration

### Changing the Vision Model

If the current Groq vision model becomes unavailable:

1. Check available models at https://console.groq.com/docs/models
2. Update `.env` file:
   ```
   GROQ_MODEL=new_vision_model_name
   ```
3. Restart the application:
   ```bash
   streamlit run app.py
   ```

The application will validate the model on startup and provide a clear error if the model is unavailable.

### Changing the Region Database

Edit the `REGIONS` dictionary in `app.py` to add or update:

- New regions
- Region-specific disposal instructions
- Local program information

---

## 🛡️ Security & Privacy

### API Security
- API keys are **never hardcoded** in the source code
- Use environment variables or Streamlit secrets
- Never commit `.env` files to version control

### Privacy
- **No user accounts required** for the MVP
- **Images are not permanently stored** on the server
- Uploaded images are sent to Groq API only for analysis
- Session data (not including images) is stored locally in browser state

### Best Practices
- Always use HTTPS in production
- Rotate API keys regularly
- Monitor API usage for suspicious activity

---

## ⚠️ Limitations & Disclaimer

### Confidence & Accuracy
- AI classifications are **guidance only**, not guarantees
- Visual identification has inherent limitations (lighting, angle, partial view, etc.)
- Always verify classifications with your local waste authority

### Regional Rules
- Waste categories and acceptance vary significantly by location
- What's recyclable in one area may not be accepted elsewhere
- Always check your **local municipal waste authority** for definitive rules

### Hazardous Items
- If an item might be dangerous, prioritize safety over convenience
- Follow local hazardous waste disposal guidelines
- When in doubt, contact your local waste authority

---

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY not configured"
**Solution**: Make sure you've created a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your real API key
```

### Error: "Vision model not found"
**Solution**: The model name might have changed. Check available models:
1. Visit https://console.groq.com/docs/models
2. Find the current vision model name
3. Update `GROQ_MODEL` in `.env`
4. Restart the app

### Error: "Could not connect to Groq API"
**Solution**: 
- Check your internet connection
- Verify your API key is valid
- Ensure the API quota hasn't been exceeded
- Check Groq status at https://status.groq.com

### Image upload fails
**Solution**:
- Supported formats: JPG, JPEG, PNG, WEBP
- Maximum file size: 10MB
- Try resizing or converting the image
- Ensure the image is not corrupted

### App runs slowly
**Solution**:
- The first request may take longer (API cold start)
- Large images are automatically compressed
- Ensure your internet connection is stable
- Try a simpler/clearer photo

---

## 📊 How It Works (Technical Overview)

### Architecture Flow

```
User Image Upload
        ↓
Image Validation & Compression
        ↓
Convert to Base64 Encoding
        ↓
Send to Groq Vision API
        ↓
AI Analysis & Classification
        ↓
JSON Parsing
        ↓
Display Results with Confidence, Safety, & Regional Guidance
        ↓
Add to Session History & Statistics
```

### AI Prompt Engineering

The application uses a carefully crafted prompt that instructs the AI to:

1. Identify the waste item accurately
2. Classify into one of 6 categories
3. Assess confidence (High/Medium/Low)
4. Flag safety concerns
5. Provide disposal instructions
6. Return structured JSON

This ensures consistent, reliable results.

---

## 🤝 Contributing

This is an open-source hackathon project. Contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- Additional regions and waste guidance
- Improved UI/UX design
- Additional languages
- Enhanced AI prompting
- Testing & bug fixes
- Documentation improvements

---

## 📝 License

This project is open-source and available under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Groq** for the powerful vision API
- **Streamlit** for the excellent web framework
- **Open source community** for incredible libraries

---

## 📧 Support & Feedback

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join discussions on GitHub Discussions
- **Email**: For direct inquiries, reach out to the team

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended for MVP)

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Add secrets in the Streamlit Cloud dashboard:
   ```
   GROQ_API_KEY = your_actual_key
   GROQ_MODEL = llama-2-vision-13b
   ```
5. Deploy!

### Deploy to Other Platforms

EcoSort AI can be deployed to:

- **Heroku** (with Procfile)
- **AWS** (with Lambda/EC2)
- **Google Cloud Run**
- **Azure App Service**
- **DigitalOcean**
- **Self-hosted servers**

---

## 📚 Resources

- [Groq API Documentation](https://console.groq.com/docs/api-overview)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Documentation](https://docs.python.org/3/)
- [Waste Management Guidelines](https://www.epa.gov/waste)

---

## 🎓 Learning from EcoSort AI

This project demonstrates:

- **AI/ML Integration**: Using vision APIs effectively
- **Prompt Engineering**: Structured AI responses
- **Full-Stack Development**: Frontend, backend, APIs
- **Error Handling**: Graceful degradation
- **UX Design**: Simple, user-focused interfaces
- **Open Source**: Collaborative development

---

**Made with 🌱 for a sustainable future.**

**EcoSort AI — From 'What is this?' to 'What should I do with it?'**
