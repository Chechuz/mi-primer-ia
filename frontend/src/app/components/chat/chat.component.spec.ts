import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatComponent } from './chat.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ApiService } from '../../services/api.service';
import { MatSelectModule } from '@angular/material/select';
import { of } from 'rxjs';

describe('ChatComponent', () => {
  let component: ChatComponent;
  let fixture: ComponentFixture<ChatComponent>;
  let apiService: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    const apiServiceSpy = jasmine.createSpyObj('ApiService', ['chat', 'upload', 'summarize', 'translate']);

    await TestBed.configureTestingModule({
      declarations: [ChatComponent],
      imports: [
        HttpClientTestingModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        FormsModule,
        MatSelectModule
      ],
      providers: [{ provide: ApiService, useValue: apiServiceSpy }]
    }).compileComponents();

    fixture = TestBed.createComponent(ChatComponent);
    component = fixture.componentInstance;
    apiService = TestBed.inject(ApiService) as jasmine.SpyObj<ApiService>;
    fixture.detectChanges();
  });

  //testChatSuccess
  it('debería enviar un mensaje y recibir una respuesta', () => {
    // Simular la respuesta del servicio
    apiService.chat.and.returnValue(of({ response: 'Hola, usuario' }));
  
    // Configurar el mensaje del usuario
    component.message = 'Hola, ¿cómo estás?';
  
    // Ejecutar el método sendMessage
    component.sendMessage();
  
    // Verificar que el método del servicio fue llamado correctamente
    expect(apiService.chat).toHaveBeenCalledWith('Hola, ¿cómo estás?');
  
    // Verificar que el historial de chat contiene el mensaje del usuario y la respuesta
    expect(component.chatHistory).toEqual([
      { sender: 'user', content: 'Hola, ¿cómo estás?' },
      { sender: 'ollama', content: 'Hola, usuario' }
    ]);
  });
  
});

