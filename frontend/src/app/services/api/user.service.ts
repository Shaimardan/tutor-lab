import { Injectable } from '@angular/core';
import { AuthorizationService } from '../../openapi/services/authorization.service';
import { BehaviorSubject, catchError, of, switchMap } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  userTrigger = new BehaviorSubject('');

  user$ = this.userTrigger.pipe(
    switchMap(() =>
      this.apiService.readUsersMeApiAuthUsersMeGet({}).pipe(
        catchError(() => {
          return of(null);
        }),
      ),
    ),
  );

  constructor(
    private apiService: AuthorizationService,
    private router: Router,
  ) {}

  logout() {
    this.apiService.logoutApiAuthLogoutPost().subscribe(() => {
      localStorage.removeItem('token');
      this.userTrigger.next('');
      this.router.navigate(['/login']);
    });
  }

  login(username: string, password: string) {
    this.apiService.loginApiAuthTokenPost({ body: { username, password } }).subscribe((x) => {
      localStorage.setItem('token', x?.['access_token'] || '');
      this.userTrigger.next('');
      this.router.navigate(['/']);
    });
  }
}
