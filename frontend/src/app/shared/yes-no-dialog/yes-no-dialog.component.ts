import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import {
  MatDialogActions,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { Inject } from '@angular/core';

export interface DialogYesNoData {
  mat_dialog_content?: string;
  mat_dialog_title?: string;
  mat_dialog_no_button_word?: string;
  mat_dialog_yes_button_word?: string;
}

@Component({
  selector: 'app-yes-no-dialog',
  templateUrl: './yes-no-dialog.component.html',
  styleUrls: ['./yes-no-dialog.component.scss'],
  standalone: true,
  imports: [MatButtonModule, MatDialogActions, MatDialogTitle, MatDialogContent],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class YesNoDialogComponent {
  public dialogData: DialogYesNoData;

  readonly dialogRef = inject(MatDialogRef<YesNoDialogComponent>);

  constructor(@Inject(MAT_DIALOG_DATA) data?: DialogYesNoData) {
    if (data) {
      this.dialogData = {
        mat_dialog_title: data.mat_dialog_title ?? 'Подтверждение действия',
        mat_dialog_content: data.mat_dialog_content ?? '',
        mat_dialog_yes_button_word: data.mat_dialog_yes_button_word ?? 'Да',
        mat_dialog_no_button_word: data.mat_dialog_no_button_word ?? 'Нет',
      };
    } else {
      this.dialogData = {
        mat_dialog_title: 'Подтверждение действия',
        mat_dialog_content: '',
        mat_dialog_no_button_word: 'Нет',
        mat_dialog_yes_button_word: 'Да',
      };
    }
  }

  onNoClick(): void {
    this.dialogRef.close(false);
  }

  onYesClick(): void {
    this.dialogRef.close(true);
  }
}
