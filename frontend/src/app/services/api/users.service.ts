import { Injectable } from '@angular/core';
import { UsersService as OpenApiUserService } from '../../openapi/services/users.service';

import { BehaviorSubject, catchError, of, switchMap } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class UsersService {
  usersListTrigger$ = new BehaviorSubject('');

  usersList$ = this.usersListTrigger$.pipe(
    switchMap(() =>
      this.apiService.getAllUsersApiUsersGet().pipe(
        catchError(() => {
          return of(null);
        }),
      ),
    ),
  );

  constructor(
    private apiService: OpenApiUserService,
    private router: Router,
  ) {}
}
