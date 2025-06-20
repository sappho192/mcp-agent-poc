import React, { useState, useRef, useEffect } from 'react';
import './App.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: Date;
  image?: string;
}

interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim() && !selectedImage) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
      image: imagePreview || undefined
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Construct message with multimodal content
      let messageContent = inputText;
      if (selectedImage && imagePreview) {
        messageContent += `\n\n[Image attached: ${selectedImage.name}]`;
        // In a real implementation, you would process the image
        // For now, we just indicate an image was attached
      }

      const response = await fetch('http://localhost:8001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageContent,
          reset_memory: false
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.success ? data.response : `Error: ${data.error || 'Unknown error occurred'}`,
        sender: 'agent',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `Connection error: ${error instanceof Error ? error.message : 'Unknown error'}. Make sure the backend server is running on port 8001.`,
        sender: 'agent',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputText('');
      removeImage();
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const resetConversation = async () => {
    try {
      await fetch('http://localhost:8001/reset', { method: 'POST' });
      setMessages([]);
    } catch (error) {
      console.error('Failed to reset conversation:', error);
    }
  };

  return (
    <div className="App">
      <header className="chat-header">
        <h1>MCP Agent Chat</h1>
        <button onClick={resetConversation} className="reset-button">
          Reset Conversation
        </button>
      </header>

      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-content">
                {message.image && (
                  <img
                    src={message.image}
                    alt="User upload"
                    className="message-image"
                  />
                )}
                <p>{message.text}</p>
                <small className="timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </small>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message agent">
              <div className="message-content">
                <p>Thinking...</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          {imagePreview && (
            <div className="image-preview">
              <img src={imagePreview} alt="Preview" />
              <button onClick={removeImage} className="remove-image">
                ×
              </button>
            </div>
          )}
          
          <div className="input-row">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              ref={fileInputRef}
              style={{ display: 'none' }}
            />
            
            <button
              onClick={() => fileInputRef.current?.click()}
              className="image-button"
              title="Add image"
            >
              📎
            </button>
            
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message..."
              className="message-input"
              rows={1}
            />
            
            <button
              onClick={sendMessage}
              disabled={isLoading || (!inputText.trim() && !selectedImage)}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
