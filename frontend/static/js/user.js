// User handling functionality

class User {
    constructor() {
        this.userId = null;
        this.userData = null;
        this.isRegistered = false;
        this.conversationIds = [];
        this.activeConversationId = null;

        // DOM elements
        this.userIdInput = document.getElementById('user-id');
        this.userForm = document.getElementById('user-form');
        this.notificationArea = document.getElementById('notification-area');
        this.conversationListContainer = document.getElementById('conversation-list-container');
        this.conversationList = document.getElementById('conversation-list');
        this.firstNameInput = document.getElementById('first-name');
        this.lastNameInput = document.getElementById('last-name');
        this.birthDateInput = document.getElementById('birth-date');
        this.genderInput = document.getElementById('gender');
        this.nationalityInput = document.getElementById('nationality');
        this.submitButton = document.getElementById('submit-user-info');

        this.initEventListeners();
    }

    initEventListeners() {
        // User ID input event
        this.userIdInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.checkUserId();
            }
        });

        // User form submit event
        this.userForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitUserForm();
        });
    }

    async checkUserId() {
        const userId = this.userIdInput.value.trim();
        
        if (!userId) {
            this.showNotification('Please enter a User ID', 'error');
            return;
        }

        this.showNotification('Checking User ID...', 'info');
        
        try {
            const response = await API.checkUserId(userId);
            
            this.userId = userId;
            this.isRegistered = response.existed;
            
            if (response.existed) {
                // Existing user
                this.userData = {
                    first_name: response.first_name,
                    last_name: response.last_name,
                    birth: response.birth,
                    gender: response.gender,
                    nationality: response.nationality
                };
                
                this.conversationIds = response.conversation_ids || [];
                
                // Fill user form with existing data
                this.fillUserForm();
                
                this.showNotification('User found! Welcome back.', 'success');
                
                // Show conversation list if any
                if (this.conversationIds.length > 0) {
                    this.updateConversationList();
                }
                
                // Enable chat interface
                ChatUI.enableChatInterface();
            } else {
                // New user
                this.showNotification('User ID not found. Please fill in your information to register.', 'error');
                this.conversationIds = [];
                this.showEmptyUserForm();
            }
        } catch (error) {
            console.error('Error checking user ID:', error);
            this.showNotification('Error checking User ID. Please try again.', 'error');
        }
    }

    fillUserForm() {
        this.firstNameInput.value = this.userData.first_name;
        this.lastNameInput.value = this.userData.last_name;
        this.birthDateInput.value = this.formatDate(this.userData.birth);
        this.genderInput.value = this.userData.gender;
        this.nationalityInput.value = this.userData.nationality;
        
        // Show the form
        this.userForm.style.display = 'block';
        
        // Show conversation list container
        this.conversationListContainer.style.display = 'block';
    }

    showEmptyUserForm() {
        // Clear form inputs
        this.userForm.reset();
        
        // Show the form
        this.userForm.style.display = 'block';
        
        // Hide conversation list container as this is a new user
        this.conversationListContainer.style.display = 'none';
    }

    async submitUserForm() {
        const userData = {
            user_id: this.userId,
            first_name: this.firstNameInput.value.trim(),
            last_name: this.lastNameInput.value.trim(),
            birth: this.birthDateInput.value,
            gender: this.genderInput.value,
            nationality: this.nationalityInput.value.trim()
        };

        if (!this.validateUserData(userData)) {
            return;
        }

        try {
            if (!this.isRegistered) {
                // Register new user
                this.showNotification('Registering user...', 'info');
                const response = await API.registerUser(userData);
                
                if (response.success) {
                    this.isRegistered = true;
                    this.userData = userData;
                    this.showNotification('Registration successful!', 'success');
                    
                    // Enable chat interface
                    ChatUI.enableChatInterface();
                    
                    // Show conversation list container, but it will be empty for new users
                    this.conversationListContainer.style.display = 'block';
                } else {
                    this.showNotification('Registration failed. Please try again.', 'error');
                }
            } else {
                // Update existing user info if needed
                this.showNotification('User information updated.', 'success');
            }
        } catch (error) {
            console.error('Error submitting user form:', error);
            this.showNotification('Error processing your request. Please try again.', 'error');
        }
    }

    validateUserData(userData) {
        if (!userData.first_name) {
            this.showNotification('Please enter your first name.', 'error');
            return false;
        }
        
        if (!userData.last_name) {
            this.showNotification('Please enter your last name.', 'error');
            return false;
        }
        
        if (!userData.birth) {
            this.showNotification('Please enter your birth date.', 'error');
            return false;
        }
        
        if (!userData.nationality) {
            this.showNotification('Please enter your nationality.', 'error');
            return false;
        }
        
        return true;
    }

    updateConversationList() {
        // Show conversation list container
        this.conversationListContainer.style.display = 'block';
        
        // Clear existing items
        this.conversationList.innerHTML = '';
        
        // Add conversation items
        this.conversationIds.forEach(conversationId => {
            const item = document.createElement('div');
            item.className = 'conversation-item';
            item.dataset.id = conversationId;
            item.textContent = `Conversation ${conversationId.substring(0, 8)}`;
            
            item.addEventListener('click', () => {
                ConversationManager.selectConversation(conversationId);
            });
            
            this.conversationList.appendChild(item);
        });
    }

    addConversation(conversationId) {
        this.conversationIds.push(conversationId);
        
        // Update the conversation list display
        this.updateConversationList();
        
        // Set as active conversation
        ConversationManager.selectConversation(conversationId);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Clear existing notifications
        this.notificationArea.innerHTML = '';
        
        // Add new notification
        this.notificationArea.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    formatDate(dateString) {
        // Handle different date formats
        if (!dateString) return '';
        
        try {
            // For 'YYYY-MM-DD' format
            if (dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
                return dateString;
            }
            
            // For Python date object or other formats
            const date = new Date(dateString);
            return date.toISOString().split('T')[0];
        } catch (error) {
            console.error('Error formatting date:', error);
            return '';
        }
    }
}
