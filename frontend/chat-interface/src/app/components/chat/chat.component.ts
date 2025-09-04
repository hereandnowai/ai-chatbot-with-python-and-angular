import { Component, signal, computed, inject, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { ChatService, ChatMessage, ChatResponse, FileUploadResponse } from '../../services/chat.service';
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
    @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

    private readonly chatService = inject(ChatService);

    protected readonly messages = signal<ChatMessage[]>([]);
    protected readonly messageControl = new FormControl('', [Validators.required]);
    protected readonly isLoading = signal(false);
    protected readonly isConnected = signal(false);
    protected readonly selectedFile = signal<File | null>(null);
    protected readonly dragOver = signal(false);

    protected readonly canSend = computed(() =>
        (this.messageControl.valid || this.selectedFile()) && !this.isLoading()
    );

    protected readonly supportedFileTypes = ['.pdf', '.txt', '.docx', '.csv'];
    protected readonly maxFileSize = 10 * 1024 * 1024; // 10MB

    constructor() {
        this.checkConnection();
        this.addWelcomeMessage();
        // Set initial connection to true and retry if needed
        setTimeout(() => {
            if (!this.isConnected()) {
                this.checkConnection();
            }
        }, 1000);
    }

    ngAfterViewChecked() {
        this.scrollToBottom();
    }

    private checkConnection() {
        this.chatService.checkHealth().subscribe({
            next: () => {
                this.isConnected.set(true);
                console.log('Backend connection: OK');
            },
            error: (error) => {
                this.isConnected.set(false);
                console.log('Backend connection failed:', error);
                // Retry after 2 seconds
                setTimeout(() => {
                    this.chatService.checkHealth().subscribe({
                        next: () => this.isConnected.set(true),
                        error: () => console.log('Retry connection failed, will update on next API call')
                    });
                }, 2000);
            }
        });
    }

    private addWelcomeMessage() {
        const welcomeMessage: ChatMessage = {
            id: crypto.randomUUID(),
            text: 'Hello! I\'m HereAndNow AI Assistant, your Angular development expert. Ask me anything about Angular v20+ best practices! 🚀\n\nYou can also upload documents (PDF, TXT, DOCX, CSV) for analysis.',
            sender: 'bot',
            timestamp: new Date()
        };
        this.messages.update(messages => [...messages, welcomeMessage]);
    }

    protected sendMessage() {
        const messageText = this.messageControl.value?.trim();
        const file = this.selectedFile();

        if ((!messageText && !file) || this.isLoading()) return;

        // Create user message
        const userMessage: ChatMessage = {
            id: crypto.randomUUID(),
            text: messageText || 'Analyzing uploaded file...',
            sender: 'user',
            timestamp: new Date(),
            fileInfo: file ? {
                name: file.name,
                type: file.type,
                size: file.size
            } : undefined
        };

        this.messages.update(messages => [...messages, userMessage]);
        this.messageControl.setValue('');
        this.isLoading.set(true);

        // Choose appropriate service method
        if (file) {
            this.chatService.sendMessageWithFile(file, messageText || 'Please analyze this file.').subscribe({
                next: (response: FileUploadResponse) => {
                    this.isConnected.set(true); // Update connection status on success
                    const botMessage: ChatMessage = {
                        id: crypto.randomUUID(),
                        text: response.message,
                        sender: 'bot',
                        timestamp: new Date()
                    };
                    this.messages.update(messages => [...messages, botMessage]);
                    this.isLoading.set(false);
                    this.clearFile();
                },
                error: (error: any) => {
                    this.isConnected.set(false); // Update connection status on error
                    const errorMessage: ChatMessage = {
                        id: crypto.randomUUID(),
                        text: 'Sorry, I encountered an error. Please try again.',
                        sender: 'bot',
                        timestamp: new Date()
                    };
                    this.messages.update(messages => [...messages, errorMessage]);
                    this.isLoading.set(false);
                    this.clearFile();
                    console.error('Chat error:', error);
                }
            });
        } else {
            this.chatService.sendMessage(messageText!).subscribe({
                next: (response: ChatResponse) => {
                    this.isConnected.set(true); // Update connection status on success
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
                    this.isConnected.set(false); // Update connection status on error
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
    }

    protected onFileSelected(event: Event) {
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];

        if (file) {
            this.validateAndSetFile(file);
        }

        // Reset the input value to allow selecting the same file again
        target.value = '';
    }

    protected onFileDrop(event: DragEvent) {
        event.preventDefault();
        this.dragOver.set(false);

        const files = event.dataTransfer?.files;
        if (files && files.length > 0) {
            this.validateAndSetFile(files[0]);
        }
    }

    protected onDragOver(event: DragEvent) {
        event.preventDefault();
        this.dragOver.set(true);
    }

    protected onDragLeave(event: DragEvent) {
        event.preventDefault();
        this.dragOver.set(false);
    }

    private validateAndSetFile(file: File) {
        // Check file size
        if (file.size > this.maxFileSize) {
            this.showError('File size must be less than 10MB');
            return;
        }

        // Check file type
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
        if (!this.supportedFileTypes.includes(fileExtension)) {
            this.showError(`Unsupported file type. Supported types: ${this.supportedFileTypes.join(', ')}`);
            return;
        }

        this.selectedFile.set(file);
    }

    private showError(message: string) {
        const errorMessage: ChatMessage = {
            id: crypto.randomUUID(),
            text: message,
            sender: 'bot',
            timestamp: new Date()
        };
        this.messages.update(messages => [...messages, errorMessage]);
    }

    protected clearFile() {
        this.selectedFile.set(null);
    }

    protected triggerFileInput() {
        this.fileInput.nativeElement.click();
    }

    protected formatFileSize(bytes: number): string {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
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
        this.clearFile();
        this.addWelcomeMessage();
    }

    protected isDragOver(): boolean {
        return this.dragOver();
    }
}
