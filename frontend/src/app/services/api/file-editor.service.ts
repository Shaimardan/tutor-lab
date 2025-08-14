import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { AssetFileSystemModelInDb } from '../../openapi/models';

@Injectable({
  providedIn: 'root',
})
export class FileEditorService {
  pickedFile$ = new BehaviorSubject<AssetFileSystemModelInDb | null>(null);

  openFile(file: AssetFileSystemModelInDb) {
    this.pickedFile$.next(file);
  }
}
