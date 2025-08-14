import { Component, OnDestroy, HostListener } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './openapi/services';
import { UserService } from './services/api/user.service';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { debounceTime, takeUntil } from 'rxjs/operators';
import { AvailabilitiesService } from './services/api/availabilities.service';
import { HeaderComponent } from '../app/shared/header/header.component';
import { FooterComponent } from '../app/shared/footer/footer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, HeaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnDestroy {
  private onDestroy$ = new Subject<void>();

  private scrollEvent$ = new Subject<void>();

  isScrolled = false;

  isHeaderVisible = true;

  user$ = this.userService.user$;

  title = 'Tutor Lab';

  isUsersPageAvailable$ = this.availabilitiesService.isUsersPageAvailable$;

  constructor(
    private apiService: ApiService,
    private userService: UserService,
    private availabilitiesService: AvailabilitiesService,
  ) {
    // eslint-disable-next-line no-console
    this.apiService.pingApiPingGet().subscribe((x) => console.info('pingApiPingGet', x));
    this.scrollEvent$.pipe(debounceTime(50), takeUntil(this.onDestroy$)).subscribe(() => {
      const scrollTop =
        window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
      if (this.isHeaderVisible == false) {
        this.isScrolled = scrollTop > 29;
      } else {
        this.isScrolled = scrollTop > 50;
      }

      if (this.isScrolled && this.isHeaderVisible) {
        this.isHeaderVisible = false;
      } else if (!this.isScrolled && !this.isHeaderVisible) {
        this.isHeaderVisible = true;
      }
    });
  }

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.scrollEvent$.next();
  }

  showHeader() {
    this.isHeaderVisible = true;
  }

  ngOnDestroy() {
    this.onDestroy$.next();
    this.onDestroy$.complete();
  }
}
