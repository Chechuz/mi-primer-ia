import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  message: string = ''; // Mensaje que el usuario escribirá
  chatHistory: { sender: string, content: string }[] = []; // Historial de mensajes

  @ViewChild('fileInput') fileInput!: ElementRef;
  selectedLanguage: string = 'es'; // Idioma seleccionado por defecto
  languages = [
    { code: 'es', name: 'Español' },
    { code: 'en', name: 'Inglés' },
    { code: 'fr', name: 'Francés' },
    { code: 'de', name: 'Alemán' },
    { code: 'it', name: 'Italiano' }
  ];

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    console.log('ChatComponent initialized.');
  }

  sendMessage(): void {
    if (this.message.trim()) {
      // Añadir el mensaje del usuario al historial
      this.chatHistory.push({ sender: 'user', content: this.message });

      // Enviar mensaje al back-end
      this.apiService.chat(this.message).subscribe(
        (data: any) => {
          // Añadir la respuesta de Ollama al historial
          this.chatHistory.push({ sender: 'ollama', content: data.response });
          this.message = ''; // Limpiar el campo de entrada
        },
        (error) => {
          console.error('Error sending message:', error);
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
      this.chatHistory.push({ sender: 'user', content: `Archivo subido: ${file.name}` });
  
      this.apiService.upload(file).subscribe(
        (data: any) => {
          this.chatHistory.push({ sender: 'ollama', content: `Archivo procesado: ${data.content}` });
        },
        (error) => {
          console.error('Error uploading file:', error);
          this.chatHistory.push({ sender: 'ollama', content: 'Error al procesar el archivo.' });
        }
      );
    }
  }
  
  summarize(): void {
    if (this.message.trim()) {
      this.chatHistory.push({ sender: 'user', content: `Resumen de: "${this.message}"` });
  
      this.apiService.summarize(this.message).subscribe(
        (data: any) => {
          this.chatHistory.push({ sender: 'ollama', content: `Resumen: ${data.summary}` });
        },
        (error) => {
          console.error('Error summarizing:', error);
          this.chatHistory.push({ sender: 'ollama', content: 'Error al generar el resumen.' });
        }
      );
    }
  }
  
  translate(): void {
    if (this.message.trim()) {
      const language = this.selectedLanguage || 'es'; // Usar el idioma seleccionado o 'es' como predeterminado
  
      // Añadir la solicitud de traducción al historial
      this.chatHistory.push({ sender: 'user', content: `Traducción de: "${this.message}" al idioma: ${language}` });
  
      this.apiService.translate(this.message, language).subscribe(
        (data: any) => {
          // Añadir la traducción al historial
          this.chatHistory.push({ sender: 'ollama', content: `Traducción: ${data.translation}` });
        },
        (error) => {
          console.error('Error translating:', error);
          this.chatHistory.push({ sender: 'ollama', content: 'Error al realizar la traducción.' });
        }
      );
    } else {
      console.warn('Message cannot be empty!');
    }
  }
  
}

