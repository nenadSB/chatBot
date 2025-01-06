import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Import CommonModule
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { ChatService } from '../services/chat.service';

// Define the structure of a chat message
interface ChatMessage {
  role: string;
  content: string;
}

@Component({
  selector: 'app-chat',
  standalone: true, // Mark the component as standalone
  imports: [CommonModule, FormsModule], // Add CommonModule and FormsModule here
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
})
export class ChatComponent {
  userMessage = '';
  chatHistory: ChatMessage[] = [];

  constructor(private chatService: ChatService) {}

  sendMessage() {
    if (!this.userMessage.trim()) return;

    // Add user message to chat history
    this.chatHistory.push({ role: 'user', content: this.userMessage });

    // Send the message to the backend and handle the response
    this.chatService.sendMessage(this.userMessage).subscribe({
      next: (response) => {
        // Add chatbot response to chat history
        this.chatHistory.push({ role: 'bot', content: response.response });
        this.userMessage = ''; // Clear input field
      },
      error: (error) => {
        console.error('Error:', error);
        this.userMessage = ''; // Clear input field even if there's an error
      },
    });
  }
}
