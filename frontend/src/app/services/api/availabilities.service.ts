import { Injectable } from '@angular/core';
import { map } from 'rxjs';
import { UserService } from './user.service';
import { PortalRole } from '../../openapi/models';

@Injectable({
  providedIn: 'root',
})
export class AvailabilitiesService {
  isUsersPageAvailable$ = this.userService.user$.pipe(
    map((user) => user !== null && user.roles.includes(PortalRole.UserAdmin)),
  );

  constructor(private userService: UserService) {}
}
