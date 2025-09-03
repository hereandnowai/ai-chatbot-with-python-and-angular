import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
}

export interface ChatResponse {
    response: string;
    status: string;
}

@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private readonly http = inject(HttpClient);
    private readonly apiUrl = 'http://localhost:5000/api';

    sendMessage(message: string): Observable<ChatResponse> {
        return this.http.post<ChatResponse>(`${this.apiUrl}/chat`, {
            message: message
        });
    }

    checkHealth(): Observable<{ status: string }> {
        return this.http.get<{ status: string }>(`${this.apiUrl}/health`);
    }
}
