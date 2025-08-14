import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class PingService {
  constructor(private http: HttpClient) {
    this.http.get('http://127.0.0.1:8000/ping').subscribe();
  }
}
