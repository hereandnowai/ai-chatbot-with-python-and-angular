import { Component, signal, computed, inject, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { ChatService, ChatMessage, ChatResponse } from '../../services/chat.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-chat',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './chat.component.html',
    styleUrl: './chat.component.css'
})
export class ChatComponent implements AfterViewChecked {
    @ViewChild('messagesContainer') messagesContainer!: ElementRef;

    private readonly chatService = inject(ChatService);

    protected readonly messages = signal<ChatMessage[]>([]);
    protected readonly messageControl = new FormControl('', [Validators.required]);
    protected readonly isLoading = signal(false);
    protected readonly isConnected = signal(false);

    protected readonly canSend = computed(() =>
        this.messageControl.valid && !this.isLoading()
    );

    constructor() {
        this.checkConnection();
        this.addWelcomeMessage();
    }

    ngAfterViewChecked() {
        this.scrollToBottom();
    }

    private checkConnection() {
        this.chatService.checkHealth().subscribe({
            next: () => this.isConnected.set(true),
            error: () => this.isConnected.set(false)
        });
    }

    private addWelcomeMessage() {
        const welcomeMessage: ChatMessage = {
            id: crypto.randomUUID(),
            text: 'Hello! I\'m HereAndNow AI Assistant, your Angular development expert. Ask me anything about Angular v20+ best practices! 🚀',
            sender: 'bot',
            timestamp: new Date()
        };
        this.messages.update(messages => [...messages, welcomeMessage]);
    }

    protected sendMessage() {
        const messageText = this.messageControl.value?.trim();
        if (!messageText || this.isLoading()) return;

        // Add user message
        const userMessage: ChatMessage = {
            id: crypto.randomUUID(),
            text: messageText,
            sender: 'user',
            timestamp: new Date()
        };

        this.messages.update(messages => [...messages, userMessage]);
        this.messageControl.setValue('');
        this.isLoading.set(true);

        // Send to API
        this.chatService.sendMessage(messageText).subscribe({
            next: (response: ChatResponse) => {
                const botMessage: ChatMessage = {
                    id: crypto.randomUUID(),
                    text: response.response,
                    sender: 'bot',
                    timestamp: new Date()
                };
                this.messages.update(messages => [...messages, botMessage]);
                this.isLoading.set(false);
            },
            error: (error: any) => {
                const errorMessage: ChatMessage = {
                    id: crypto.randomUUID(),
                    text: 'Sorry, I encountered an error. Please try again.',
                    sender: 'bot',
                    timestamp: new Date()
                };
                this.messages.update(messages => [...messages, errorMessage]);
                this.isLoading.set(false);
                console.error('Chat error:', error);
            }
        });
    }

    protected onKeyPress(event: KeyboardEvent) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    private scrollToBottom() {
        if (this.messagesContainer) {
            const element = this.messagesContainer.nativeElement;
            element.scrollTop = element.scrollHeight;
        }
    }

    protected clearChat() {
        this.messages.set([]);
        this.addWelcomeMessage();
    }
}
