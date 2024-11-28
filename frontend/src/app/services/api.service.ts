import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) { }

    // Método para enviar un mensaje al back-end
    chat(message: string): Observable<any> {
      const url = `${this.baseUrl}/chat`; // Endpoint para el chat
      return this.http.post(url, { message });
    }
    upload(file: File): Observable<any> {
      const url = `${this.baseUrl}/upload`;
      const formData = new FormData();
      formData.append('file', file);
      return this.http.post(url, formData);
    }
    
    summarize(text: string): Observable<any> {
      const url = `${this.baseUrl}/summarize`;
      return this.http.post(url, { text });
    }
    
    translate(text: string, language: string): Observable<any> {
      const url = `${this.baseUrl}/translate`;
      return this.http.post(url, { text, language });
    }
    
}
