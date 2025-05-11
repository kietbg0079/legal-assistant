// Chat interface functionality

class ChatUI {
    static chatContainer = document.getElementById('chat-container');
    static welcomeMessage = document.getElementById('welcome-message');
    static messagesContainer = document.getElementById('chat-messages');
    static messageInput = document.getElementById('message-input');
    static sendButton = document.getElementById('send-button');
    static newConversationBtn = document.getElementById('new-conversation-btn');

    static init() {
        // Initialize event listeners
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        this.newConversationBtn.addEventListener('click', () => {
            this.createNewConversation();
        });
    }

    static enableChatInterface() {
        // Hide welcome message and show chat container
        this.welcomeMessage.style.display = 'none';
        this.chatContainer.style.display = 'flex';
    }
    
    static sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            return;
        }
        
        // Clear input field
        this.messageInput.value = '';
        
        // Send message through conversation manager
        ConversationManager.sendMessage(message);
    }
    
    static async createNewConversation() {
        if (!userManager.userId) {
            userManager.showNotification('Please enter a User ID first', 'error');
            return;
        }
        
        // Create new conversation
        await ConversationManager.createConversation(userManager.userId);
        
        // Clear messages
        this.clearMessages();
    }
    
    static addMessage(content, role) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${role}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        messageContent.textContent = content;
        
        messageElement.appendChild(messageContent);
        this.messagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    static clearMessages() {
        this.messagesContainer.innerHTML = '';
    }
    
    static showLoadingMessage() {
        const loadingElement = document.createElement('div');
        loadingElement.className = 'message bot loading';
        loadingElement.innerHTML = '<div class="message-content">Loading conversation history...</div>';
        
        this.messagesContainer.appendChild(loadingElement);
    }
    
    static showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.className = 'message bot typing';
        typingElement.innerHTML = '<div class="message-content">Typing<span class="dot-typing">...</span></div>';
        
        this.messagesContainer.appendChild(typingElement);
        this.scrollToBottom();
    }
    
    static hideTypingIndicator() {
        const typingElements = document.querySelectorAll('.typing');
        typingElements.forEach(element => element.remove());
    }
    
    static scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}