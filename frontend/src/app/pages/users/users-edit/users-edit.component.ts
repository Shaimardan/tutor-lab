import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { UsersService } from '../../../services/api/users.service';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { ActivatedRoute } from '@angular/router';
import { combineLatest, map } from 'rxjs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatSelectModule } from '@angular/material/select';
import { UsersService as OpenApiUserService } from '../../../openapi/services/users.service';

@Component({
  selector: 'app-users-edit',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatInputModule,
    MatButtonModule,
    MatTableModule,
    MatIconModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    MatSelectModule,
  ],
  templateUrl: './users-edit.component.html',
  styleUrl: './users-edit.component.scss',
})
export class UsersEditComponent {
  password = '';

  passwordConfirm = '';

  private userId$ = this.activateRoute.params.pipe(map((x) => x['id']));

  private users$ = this.usersService.usersList$;

  roles$ = this.apiService.getAllRolesApiUsersAllRolesGet();

  user$ = combineLatest([this.users$, this.userId$]).pipe(
    map(([users, userId]) => users?.find((x) => x.id.toString() === userId.toString())),
  );

  constructor(
    private usersService: UsersService,
    private activateRoute: ActivatedRoute,
    private apiService: OpenApiUserService,
  ) {
    this.usersService.usersListTrigger$.next('');
  }
}
