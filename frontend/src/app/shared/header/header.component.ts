import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { UserService } from '../../services/api/user.service';
import { AvailabilitiesService } from '../../services/api/availabilities.service';

import { trigger, transition, style, animate } from '@angular/animations';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    RouterLink,
    CommonModule,
    MatButtonModule,
    MatToolbarModule,
    MatMenuModule,
    MatIconModule,
    RouterModule,
  ],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  animations: [
    trigger('slideInOut', [
      transition(':enter', [
        style({ transform: 'translateY(-100%)' }),
        animate('300ms ease-in-out', style({ transform: 'translateY(0%)' })),
      ]),
      transition(':leave', [
        animate('300ms ease-in-out', style({ transform: 'translateY(-100%)' })),
      ]),
    ]),
  ],
})
export class HeaderComponent {
  @Input() isVisible = true;

  @Input() isScrolled = false;

  user$ = this.userService.user$;

  isUsersPageAvailable$ = this.availabilitiesService.isUsersPageAvailable$;

  isMenuRaised: boolean = false;

  onClickMenu(): void {
    this.isMenuRaised = !this.isMenuRaised;
  }

  constructor(
    private userService: UserService,
    private availabilitiesService: AvailabilitiesService,
  ) {}

  logout() {
    this.userService.logout();
  }
}
