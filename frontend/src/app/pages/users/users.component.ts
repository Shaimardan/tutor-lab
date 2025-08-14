import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { UsersService } from '../../services/api/users.service';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatInputModule,
    MatButtonModule,
    MatTableModule,
    MatIconModule,
  ],
  templateUrl: './users.component.html',
  styleUrl: './users.component.scss',
})
export class UsersComponent {
  displayedColumns: string[] = [
    // 'user_id',
    'username',
    'fullname',
    'email',
    'roles',
    'edit',
  ];

  users$ = this.usersService.usersList$;

  constructor(private usersService: UsersService) {
    this.usersService.usersListTrigger$.next('');
  }
}
