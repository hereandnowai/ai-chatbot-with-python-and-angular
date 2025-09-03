import { Component, signal, inject, OnInit } from '@angular/core';
import { ChatComponent } from './components/chat/chat.component';
import { BrandingService, Branding } from './services/branding.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ChatComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent implements OnInit {
  private readonly brandingService = inject(BrandingService);
  protected readonly branding = signal<Branding | null>(null);

  ngOnInit() {
    this.brandingService.getBranding().subscribe({
      next: (branding) => this.branding.set(branding),
      error: (error) => console.error('Failed to load branding:', error)
    });
  }
}
