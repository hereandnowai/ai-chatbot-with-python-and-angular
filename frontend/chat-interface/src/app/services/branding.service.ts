import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Branding {
    organization: string;
    website: string;
    email: string;
    mobile: string;
    slogan: string;
    logo_title: string;
    logo_favicon: string;
    github: string;
}

@Injectable({
    providedIn: 'root'
})
export class BrandingService {
    private readonly http = inject(HttpClient);

    getBranding(): Observable<Branding> {
        return this.http.get<Branding>('/branding.json');
    }
}
