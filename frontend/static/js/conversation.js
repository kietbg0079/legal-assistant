// Conversation management functionality

class ConversationManager {
    static activeConversationId = null;

    // Create a new conversation
    static async createConversation(userId) {
        try {
            const response = await API.createConversation(userId);
            const conversationId = response.conversation_id;
            
            // Add the conversation to user's list
            userManager.addConversation(conversationId);
            
            return conversationId;
        } catch (error) {
            console.error('Error creating conversation:', error);
            userManager.showNotification('Failed to create a new conversation.', 'error');
            return null;
        }
    }

    // Load and display conversation history
    static async loadConversation(conversationId) {
        try {
            ChatUI.clearMessages();
            ChatUI.showLoadingMessage();
            
            const response = await API.getConversation(conversationId);
            const messages = response.messages;
            
            // Clear the loading message
            ChatUI.clearMessages();
            
            // Display the conversation history
            messages.forEach(message => {
                ChatUI.addMessage(message.content, message.role);
            });
            
            // Scroll to the bottom
            ChatUI.scrollToBottom();
            
            // Set active conversation
            this.setActiveConversation(conversationId);
            
        } catch (error) {
            console.error('Error loading conversation:', error);
            userManager.showNotification('Failed to load conversation.', 'error');
            ChatUI.clearMessages();
        }
    }

    // Send a message in the current conversation
    static async sendMessage(message) {
        if (!this.activeConversationId) {
            userManager.showNotification('No active conversation. Creating a new one...', 'info');
            
            // Create a new conversation if none exists
            this.activeConversationId = await this.createConversation(userManager.userId);
            
            if (!this.activeConversationId) {
                userManager.showNotification('Failed to create conversation.', 'error');
                return;
            }
        }
        
        try {
            // Add user message to display
            ChatUI.addMessage(message, 'user');
            
            // Show typing indicator
            ChatUI.showTypingIndicator();
            
            // Send the message to API
            const response = await API.sendChatMessage(userManager.userId, this.activeConversationId, message);
            
            // Hide typing indicator
            ChatUI.hideTypingIndicator();
            
            // Add bot response to display
            ChatUI.addMessage(response.message, 'assistant');
            
        } catch (error) {
            console.error('Error sending message:', error);
            ChatUI.hideTypingIndicator();
            userManager.showNotification('Failed to send message.', 'error');
        }
    }

    // Select a conversation from the list
    static selectConversation(conversationId) {
        if (conversationId === this.activeConversationId) {
            return; // Already selected
        }
        
        // Update active conversation
        this.loadConversation(conversationId);
    }

    // Set the active conversation and update UI
    static setActiveConversation(conversationId) {
        this.activeConversationId = conversationId;
        
        // Update conversation list UI
        const items = document.querySelectorAll('.conversation-item');
        items.forEach(item => {
            if (item.dataset.id === conversationId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
}
