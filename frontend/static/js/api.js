// API handling functions

const API_BASE_URL = 'http://localhost:1830'; // Change this to your API server URL

class API {
    // Check if a user ID exists
    static async checkUserId(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/v1/check_user_id`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error checking user ID:', error);
            
            // For testing/development, provide mock responses
            // In production, you would remove this and handle errors properly
            if (Math.random() > 0.5) {
                // Mock existing user
                return {
                    existed: true,
                    first_name: "An",
                    last_name: "Nguyen",
                    birth: "2001-09-18",
                    gender: "Male",
                    nationality: "Vietnamese",
                    conversation_ids: ["conv_uuid1", "conv_uuid2", "conv_uuid3"]
                };
            } else {
                // Mock new user
                return {
                    existed: false,
                    conversation_ids: []
                };
            }
        }
    }

    // Register a new user
    static async registerUser(userData) {
        try {
            const response = await fetch(`${API_BASE_URL}/v1/register_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error registering user:', error);
            
            // Mock response for testing
            return {
                success: true
            };
        }
    }

    // Create a new conversation
    static async createConversation(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/v1/create_conversation`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error creating conversation:', error);
            
            // Mock response for testing
            return {
                conversation_id: "conv_" + Math.random().toString(36).substring(2, 10)
            };
        }
    }

    // Get conversation history
    static async getConversation(conversationId) {
        try {
            const response = await fetch(`${API_BASE_URL}/v1/get_conversation`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ conversation_id: conversationId })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting conversation:', error);
            
            // Mock response for testing
            return [
                { role: "user", content: "Hello there" },
                { role: "bot", content: "Hi! How can I help you today?" },
                { role: "user", content: "I have a question about your service" },
                { role: "bot", content: "Sure, I'd be happy to answer any questions you have about our service. What would you like to know?" }
            ];
        }
    }

    // Send a chat message
    static async sendChatMessage(userId, conversationId, message) {
        try {
            const response = await fetch(`${API_BASE_URL}/v1/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    conversation_id: conversationId,
                    message: message
                })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error sending chat message:', error);
            
            // Mock response for testing
            return {
                conversation_id: conversationId,
                message: "This is a mock response from the chatbot. In production, this would be a real response from the API."
            };
        }
    }
}
