import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
    fileInfo?: {
        name: string;
        type: string;
        size: number;
    };
}

export interface ChatResponse {
    response: string;
    status?: string;
    filename?: string;
}

export interface FileUploadResponse {
    success: boolean;
    message: string;
    filename?: string;
}

@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private readonly http = inject(HttpClient);
    private readonly apiUrl = 'http://localhost:8001/api';

    sendMessage(message: string): Observable<ChatResponse> {
        return this.http.post<ChatResponse>(`${this.apiUrl}/chat`, {
            message: message
        });
    }

    sendMessageWithFile(file: File, message: string): Observable<FileUploadResponse> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('message', message);

        return this.http.post<FileUploadResponse>(`${this.apiUrl}/chat/upload`, formData);
    }

    checkHealth(): Observable<{ status: string }> {
        return this.http.get<{ status: string }>(`${this.apiUrl}/health`);
    }
}
