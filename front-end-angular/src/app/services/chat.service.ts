import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Define the structure of the response from the Flask backend
interface ChatResponse {
  response: string;
}

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  // Define the base URL for the Flask backend
  private apiUrl = 'http://127.0.0.1:5000/chat';

  constructor(private http: HttpClient) {}

  // Define the sendMessage method with a proper return type
  sendMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(this.apiUrl, { message });
  }
}
