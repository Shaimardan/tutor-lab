import { Routes } from '@angular/router';
import { StartPageComponent } from './pages/start-page/start-page.component';
import { LoginComponent } from './pages/login/login.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'home',
    component: StartPageComponent,
  },
];
