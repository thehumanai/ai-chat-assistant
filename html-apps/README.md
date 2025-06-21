# AI Chat Assistant

A modern, responsive web-based chat interface that supports AI conversations and file uploads.

## Features

### 🎨 Modern UI Design
- Clean, gradient-based design with smooth animations
- Responsive layout that works on desktop and mobile devices
- Beautiful message bubbles with user and AI avatars
- Smooth fade-in animations for messages

### 💬 Chat Functionality
- Real-time chat interface with typing indicators
- Support for both text messages and file uploads
- Message timestamps
- Auto-scrolling to latest messages
- Enter key to send messages (Shift+Enter for new lines)

### 📁 File Upload System
- Drag and drop file upload support
- Click to upload multiple files
- File size display and formatting
- Visual file attachments in chat
- Ability to remove files before sending
- Support for all file types

### 🤖 AI Integration Ready
- Simulated AI responses for demonstration
- Easy to integrate with real AI APIs (OpenAI, Claude, etc.)
- Context-aware responses based on user input
- Typing indicators during AI processing

## How to Use

1. **Open the Application**
   - Simply open `index.html` in any modern web browser
   - No server setup required - works offline

2. **Start Chatting**
   - Type your message in the text area
   - Press Enter or click the send button (➤)
   - The AI will respond with contextual messages

3. **Upload Files**
   - Click the "📎 Click to upload files or drag and drop" area
   - Or drag files directly onto the upload area
   - Files will appear as attachments in your message
   - Remove files by clicking the × button if needed

4. **File Management**
   - Uploaded files show name and size
   - Files are attached to your message when sent
   - AI can reference uploaded files in responses

## Technical Details

### Built With
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **Vanilla JavaScript** - No frameworks required
- **ES6 Classes** - Object-oriented design

### Browser Compatibility
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

### File Upload Features
- Multiple file selection
- Drag and drop support
- File size validation
- Visual feedback during upload
- File type agnostic

## Customization

### Styling
The application uses CSS custom properties and can be easily customized:
- Change colors by modifying the gradient values
- Adjust spacing and sizing in the CSS
- Modify animations and transitions

### AI Integration
To connect to a real AI service, replace the `generateAIResponse()` method in the JavaScript with your preferred API calls.

### File Processing
Add file processing logic in the `sendMessage()` method to handle uploaded files with your backend services.

## Future Enhancements

- [ ] Real AI API integration
- [ ] File preview capabilities
- [ ] Message history persistence
- [ ] User authentication
- [ ] Voice message support
- [ ] Image generation capabilities
- [ ] Export chat history
- [ ] Dark mode toggle

## License

This project is open source and available under the MIT License. 