import { ApplicationConfig, Injectable, Provider } from '@angular/core';
import { Router, provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {
  HTTP_INTERCEPTORS,
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  provideHttpClient,
  withInterceptorsFromDi,
} from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { Observable, catchError, throwError } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private router: Router) {
    // eslint-disable-next-line no-console
    console.info('AuthInterceptor created');
  }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    if (!request.url.startsWith('/api')) {
      return next.handle(request);
    } else {
      if (!localStorage.getItem('token')) {
        this.router.navigate(['/login'], {
          queryParams: {
            next: encodeURIComponent(window.location.href),
          },
        });
      }
      request = request.clone({
        setHeaders: {
          Authorization: 'Bearer ' + localStorage.getItem('token'),
        },
      });
    }

    return next.handle(request).pipe(
      catchError((err) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status === 401 || err.status === 403) {
            this.router.navigate(['/login'], {
              queryParams: {
                next: encodeURIComponent(window.location.href),
              },
            });
          }
        }
        return throwError(err);
      }),
    );
  }
}

export const API_INTERCEPTOR_PROVIDER: Provider = {
  provide: HTTP_INTERCEPTORS,
  useClass: AuthInterceptor,
  multi: true,
};

export const appConfig: ApplicationConfig = {
  providers: [
    API_INTERCEPTOR_PROVIDER,
    provideRouter(routes),
    provideHttpClient(withInterceptorsFromDi()),
    provideAnimationsAsync(),
  ],
};
