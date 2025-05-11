// Main entry point for application

// Global user manager instance
let userManager;

// Initialize application
function initApp() {
    console.log('Initializing Chatbot Frontend');
    
    // Initialize user manager
    userManager = new User();
    
    // Initialize chat UI
    ChatUI.init();
}

// Wait for DOM to be loaded
document.addEventListener('DOMContentLoaded', initApp);