import { MatIconModule } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';
import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

export class InfoObject {
  description: string;

  constructor(description: string) {
    this.description = description;
  }

  static fromString(infoString: string): InfoObject {
    return new InfoObject(infoString);
  }
}

@Component({
  selector: 'app-question-info',
  standalone: true,
  imports: [MatIconModule, CommonModule, MatTooltip],
  templateUrl: './question-info.component.html',
  styleUrls: ['./question-info.component.scss'],
})
export class QuestionInfoComponent {
  @Input() infoObject: InfoObject = {
    description: '',
  };
}
