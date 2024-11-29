import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  message: string = '';
  chatHistory: { sender: string, content: string }[] = [];
  isLoading: boolean = false; // Estado para mostrar animación de carga

  @ViewChild('fileInput') fileInput!: ElementRef;
  selectedLanguage: string = 'es';
  languages = [
    { code: 'es', name: 'Español' },
    { code: 'en', name: 'Inglés' },
    { code: 'fr', name: 'Francés' },
    { code: 'de', name: 'Alemán' },
    { code: 'it', name: 'Italiano' }
  ];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    console.log('ChatComponent initialized.');
  }

  sendMessage(): void {
    if (this.message.trim()) {
      this.isLoading = true;
      this.chatHistory.push({ sender: 'user', content: this.message });

      this.apiService.chat(this.message).subscribe(
        (data: any) => {
          this.chatHistory.push({ sender: 'ollama', content: data.response });
          this.message = '';
          this.isLoading = false;
        },
        (error) => {
          console.error('Error sending message:', error);
          this.isLoading = false;
        }
      );
    } else {
      console.warn('Message cannot be empty!');
    }
  }

  openFileDialog(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      this.isLoading = true;
      this.chatHistory.push({ sender: 'user', content: `Archivo subido: ${file.name}` });

      this.apiService.upload(file).subscribe(
        (data: any) => {
          this.chatHistory.push({ sender: 'ollama', content: `Archivo procesado: ${data.content}` });
          this.isLoading = false;
        },
        (error) => {
          console.error('Error uploading file:', error);
          this.chatHistory.push({ sender: 'ollama', content: 'Error al procesar el archivo.' });
          this.isLoading = false;
        }
      );
    }
  }

  summarize(): void {
    if (this.message.trim()) {
      this.isLoading = true;
      this.chatHistory.push({ sender: 'user', content: `Resumen de: "${this.message}"` });

      this.apiService.summarize(this.message).subscribe(
        (data: any) => {
          this.chatHistory.push({ sender: 'ollama', content: `Resumen: ${data.summary}` });
          this.isLoading = false;
        },
        (error) => {
          console.error('Error summarizing:', error);
          this.chatHistory.push({ sender: 'ollama', content: 'Error al generar el resumen.' });
          this.isLoading = false;
        }
      );
    }
  }

  translate(): void {
    if (this.message.trim()) {
      this.isLoading = true;
      this.chatHistory.push({ sender: 'user', content: `Traducción de: "${this.message}"` });

      this.apiService.translate(this.message, this.selectedLanguage).subscribe(
        (data: any) => {
          this.chatHistory.push({ sender: 'ollama', content: `Traducción: ${data.translation}` });
          this.isLoading = false;
        },
        (error) => {
          console.error('Error translating:', error);
          this.chatHistory.push({ sender: 'ollama', content: 'Error al realizar la traducción.' });
          this.isLoading = false;
        }
      );
    }
  }
}
